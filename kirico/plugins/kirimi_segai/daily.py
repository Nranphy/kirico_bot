from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State,CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.log import logger
from kirico.utils.file_utils import check_dir, check_file
from kirico.utils.money_utils import money_change
from kirico.utils.message_utils import send_forward_msg
from .utils import gain_exp, get_equipment_info, get_skill_info, job_text_trans, jobchange_to, read_profession, read_statu, read_bag, role_exist, save_profession, save_statu, skill_text_trans
import time
import os
import json





# 消耗雾团子购买经验
buy_exp = on_command("购买经验",aliases={"经验购买"},priority=9,block=True)

@buy_exp.handle()
async def buy_exp_process1(bot:Bot,event:Event,arg:Message = CommandArg(),state:T_State=State()):
    state["num"] = arg

@buy_exp.got("num")
async def buy_exp_process2(bot:Bot,event:Event,state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await buy_exp.finish("购买失败...你还未注册哦×\n请输入【/注册】查看详细",at_sender=True)
    arg = state["num"].extract_plain_text().strip()
    if not arg.isdigit():
        await buy_exp.finish("购买失败...数字输入格式有误×",at_sender=True)
    else: arg = int(arg)
    if arg == 0:
        await buy_exp.finish("唔...嗯...\n你是在调戏雾子吗！！",at_sender=True)
    temp = money_change(qq,-arg,0,note="购买了经验...")
    if temp[0] ==0:
        await buy_exp.finish(f"购买失败...雾团子好像不足哦×\n=========\n【当前雾团子】{temp[1]}",at_sender=True)
    else:
        level_up = gain_exp(qq,arg,0)
    msg = f"购买成功~\n=========\n【剩余雾团子】{temp[1]}\n========="
    msg += f"\n【获得经验】{level_up[0]}\n（提升{level_up[1]}级，获得点数{level_up[2]}）\n【剩余点数】{level_up[3]}" if level_up[1] else f"\n【获得经验】{level_up[0]}\n【剩余点数】{level_up[3]}"
    new_skill = '\n'.join([skill_text_trans(x)[0]+f'（{x}）' for x in level_up[5]])
    msg += f"\n=========\n【获得新技能】\n{new_skill}" if level_up[5] else ''
    new_job = '\n'.join([job_text_trans(x)+f'（{x}）' for x in level_up[6]])
    msg += f"\n=========\n【当前可转职业】\n{new_job}" if level_up[6] else ''
    await buy_exp.finish(msg+f"\n=========\n【当前等级】{level_up[4]['level']}\n【当前经验】{level_up[4]['exp']}\n【升级所需经验】{level_up[4]['needexp']}",at_sender=True)



# 素质加点
add_point = on_command("加点",aliases={"素质加点"},priority=9,block=True)

@add_point.handle()
async def add_point_process1(bot:Bot,event:Event,arg:Message = CommandArg(),state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await add_point.finish("加点失败...你还未注册哦×\n请输入【/注册】查看详细~",at_sender=True)
    command = arg.extract_plain_text().strip().split()
    try:
        which_statu = command[0]
        how_much = command[1]
    except:
        await add_point.finish("输入【/加点 XXX xxx】向XXX素质加点xxx点，请检查格式~\n素质分别为Str、Agi、Vit、Int、Dex、Luk六种...\n例子【/加点 str 10】",at_sender=True)
    if which_statu.lower()=="str" or which_statu=="力量":which_statu = "Str"
    elif which_statu.lower()=="agi" or which_statu=="敏捷":which_statu = "Agi"
    elif which_statu.lower()=="vit" or which_statu=="耐力":which_statu = "Vit"
    elif which_statu.lower()=="int" or which_statu=="智力":which_statu = "Int"
    elif which_statu.lower()=="dex" or which_statu=="灵巧":which_statu = "Dex"
    elif which_statu.lower()=="luk" or which_statu=="幸运":which_statu = "Luk"
    if which_statu not in ["Str","Agi","Vit","Int","Dex","Luk"]:
        await add_point.finish("加点失败× 未知的素质值...请注意指令顺序\n素质分别为Str、Agi、Vit、Int、Dex、Luk六种...\n例子【/加点 str 10】",at_sender=True)
    if not how_much.isdigit():
        await add_point.finish("加点失败× 加点数量非阿拉伯数字...请注意指令顺序...\n例子【/加点 str 10】",at_sender=True)
    else: how_much = int(how_much)
    statu = read_statu(qq)
    statu["point"] -= how_much
    if statu["point"]<0:
        await add_point.finish(f"加点失败× 剩余点数不够呢...\n=========\n【剩余点数】{statu['point']+how_much}",at_sender=True)
    statu[which_statu] += how_much
    try:
        save_statu(qq,statu)
    except:
        await add_point.finish("读写文件出错...请稍后再试×",at_sender=True)
    await add_point.finish(f"加点成功~ \n=========\n【剩余点数】{statu['point']}\n【{which_statu}】{statu[which_statu] -how_much} + {how_much}",at_sender=True)



# 穿上装备

wear_equipment = on_command("穿上装备",aliases={"穿戴装备","武器装备","装备武器","更换装备","装备更换","装备更改","更换武器","武器更换"},priority=7,block=True)

@wear_equipment.handle()
async def wear_equipment_process(bot:Bot,event:Event,arg:Message=CommandArg(),state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await wear_equipment.finish("你还未注册哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    state["command"] = arg.extract_plain_text().strip().split()
    if not state["command"]:
        await wear_equipment.finish("请在指令后输入你想换上的装备哦~\n例子【/穿上装备 xxx xxx】，xxx为装备id，可同时添加多个，用空格分开~",at_sender=True)
    bag_dic = read_bag(qq)
    profession_dic = read_profession(qq)
    for key in state["command"]:
        if str(key) not in bag_dic["equipment"]:
            await wear_equipment.finish(f"不能换上你未拥有的装备哦~\n出错装备序号为【{key}】",at_sender=True)
        info = get_equipment_info(key)[0]
        if profession_dic["level"] < info["limit"]["level"]:
            await wear_equipment.finish(f"你的等级未达到装备限制等级哦~\n出错装备序号为【{key}】，等级限制【{info['limit']['level']}】",at_sender=True)
        if profession_dic["job"] in info["limit"]["job"]:
            await wear_equipment.finish(f"你的职业不能穿戴此装备~\n出错装备序号为【{key}】，无法穿戴该装备的职业有【{info['limit']['job']}】",at_sender=True)
        if profession_dic["race"] in info["limit"]["race"]:
            await wear_equipment.finish(f"你的种族不能穿戴此装备~\n出错装备序号为【{key}】，无法穿戴该装备的种族有【{info['limit']['race']}】",at_sender=True)
        profession_dic["equipment"][info["place"]] = info["item"]
    save_profession(qq,profession_dic)
    equipment_info = get_equipment_info(profession_dic["equipment"])
    await wear_equipment.send("装备成功哦~"+f'''
=========
当前装备
【武器】{equipment_info[0].get("detail",{}).get("name","空")}（{equipment_info[0].get("item",'None')}）
【头部】{equipment_info[1].get("detail",{}).get("name","空")}（{equipment_info[1].get("item",'None')}）
【护具】{equipment_info[2].get("detail",{}).get("name","空")}（{equipment_info[2].get("item",'None')}）
【鞋子】{equipment_info[3].get("detail",{}).get("name","空")}（{equipment_info[3].get("item",'None')}）
【饰品】{equipment_info[4].get("detail",{}).get("name","空")}（{equipment_info[4].get("item",'None')}）
=========''',at_sender=True)

## 脱下
clear_equipment = on_command("脱下装备",aliases={"武器取下","取下武器","换下装备","装备脱下","放下武器"},priority=7,block=True)

@clear_equipment.handle()
async def clear_equipment_process(bot:Bot,event:Event,arg:Message=CommandArg(),state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await clear_equipment.finish("你还未注册哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    profession_dic = read_profession(qq)
    profession_dic["equipment"] = ['0','None','None','None','None']
    save_profession(qq,profession_dic)
    equipment_info = get_equipment_info(profession_dic["equipment"])
    await clear_equipment.send("脱下装备成功~"+f'''
=========
当前装备
【武器】{equipment_info[0].get("detail",{}).get("name","空")}（{equipment_info[0].get("item",'None')}）
【头部】{equipment_info[1].get("detail",{}).get("name","空")}（{equipment_info[1].get("item",'None')}）
【护具】{equipment_info[2].get("detail",{}).get("name","空")}（{equipment_info[2].get("item",'None')}）
【鞋子】{equipment_info[3].get("detail",{}).get("name","空")}（{equipment_info[3].get("item",'None')}）
【饰品】{equipment_info[4].get("detail",{}).get("name","空")}（{equipment_info[4].get("item",'None')}）
=========''',at_sender=True)



# 更换技能

change_skill = on_command("更换技能",aliases={"技能更换","更改技能","携带技能","技能携带","添加技能","技能添加"},priority=7,block=True)

@change_skill.handle()
async def change_skill_process(bot:Bot,event:Event,arg:Message=CommandArg(),state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await change_skill.finish("你还未注册哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    bag_dic = read_bag(qq)
    profession_dic = read_profession(qq)
    state["skill"] = arg.extract_plain_text().strip().split()
    if not state["skill"]:
        await change_skill.finish("请在指令后输入你想添加的技能哦~\n例子【/添加技能 xxx xxx】，xxx为技能英文名（注意大小写），可同时添加多个，用空格分开~",at_sender=True)
    for name in state["skill"]:
        if name not in bag_dic["skill"]:
            await change_skill.finish(f"不能添加你未拥有的技能哦~\n本指令只支持技能英文名，请注意技能名大小写~\n出错技能名为【{name}】",at_sender=True)
        info = get_skill_info(name)[0]
        if profession_dic["level"] < info["limit"]["level"]:
            await change_skill.finish(f"你的等级不足以使用该技能哦~\n出错技能名为【{name}】，等级限制【{info['limit']['level']}】",at_sender=True)
        if profession_dic["job"] in info["limit"]["job"]:
            await change_skill.finish(f"你的职业不能使用该技能~\n出错技能名为【{name}】，无法使用该技能的职业有【{info['limit']['job']}】",at_sender=True)
        if profession_dic["race"] in info["limit"]["race"]:
            await change_skill.finish(f"你的种族不能使用该技能~\n出错技能名为【{name}】，无法使用该技能的种族有【{info['limit']['race']}】",at_sender=True)
        # 技能位限制
        skill_limit_num = profession_dic["level"]//5+3
        if len(profession_dic["skill"]) > skill_limit_num:
            await change_skill.finish(f"技能超出当前角色所拥有技能位！\n当前技能位总数为【{skill_limit_num}】\n装备技能不包含在技能位中哦~",at_sender=True)
        profession_dic["skill"].append(name)
    save_profession(qq,profession_dic)
    skill_info = get_skill_info(profession_dic["skill"])
    await change_skill.send('''技能添加成功~\n=========\n【当前技能】\n'''+'\n'.join([f'{x["detail"]["transname"]} ({x["detail"]["name"]})' for x in skill_info])+"\n=========",at_sender=True)

## 取下某一个
unwear_skill = on_command("清除技能",aliases={"技能清除","技能取下","取下技能"},priority=7,block=True)

@unwear_skill.handle()
async def unwear_skill_process(bot:Bot,event:Event,arg:Message=CommandArg(),state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await unwear_skill.finish("你还未注册哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    profession_dic = read_profession(qq)
    state["skill"] = arg.extract_plain_text().strip().split()
    if not state["skill"]:
        await unwear_skill.finish("请在指令后输入你想添加的技能哦~\n例子【/添加技能 xxx xxx】，xxx为技能英文名（注意大小写），可同时添加多个，用空格分开~",at_sender=True)
    for skill in state["skill"]:
        if skill not in profession_dic["skill"]:
            await unwear_skill.finish(f"不能取下未拥有的技能！！\n出错技能名为【{skill}】",at_sender=True)
        profession_dic["skill"].remove(skill)
    save_profession(qq,profession_dic)
    skill_info = get_skill_info(profession_dic["skill"])
    await unwear_skill.send('''技能取下成功~\n=========\n【当前技能】\n'''+'\n'.join([f'{x["detail"]["transname"]} ({x["detail"]["name"]})' for x in skill_info])+"\n=========",at_sender=True)

## 全部换下
clear_skill = on_command("清空技能",aliases={"技能清空"},priority=7,block=True)

@clear_skill.handle()
async def clear_skill_process(bot:Bot,event:Event,state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await clear_skill.finish("你还未注册哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    profession_dic = read_profession(qq)
    profession_dic["skill"] = []
    save_profession(qq,profession_dic)
    await clear_skill.send("清空当前技能列表成功~\n=========\n【当前未准备任何技能】",at_sender=True)



# 转职

jobchange = on_command("转职",aliases={"职业变更","变更职业"},priority=7,block=7)

@jobchange.handle()
async def jobchange_prepare(bot:Bot, event:Event, arg:Message=CommandArg(), state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await jobchange.finish("你还未注册哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    arg = arg.extract_plain_text().strip()
    if not arg:
        await jobchange.finish("输入【/转职 xxx】进行转职哦~\nxxx为职业名称（中英皆可）",at_sender=True)
    result = jobchange_to(qq,arg)
    if not result[0]:
        await jobchange.finish(f"转职失败×\n{result[1]}",at_sender=True)
    else:
        state["job"] = arg
        await jobchange.send(f"当前可以转职为【{arg}】哦~\n是否要进行转职呢？\n输入【yes】或者【是】进行确认。",at_sender=True)

@jobchange.got("ok")
async def jobchange_process(bot:Bot, event:Event, state:T_State=State()):
    qq = event.get_user_id()
    state["ok"] = state["ok"].extract_plain_text().strip()
    if state["ok"] != "是" and state["ok"] != "yes":
        await jobchange.finish(f"已取消转职×\n下次再来吧~",at_sender=True)
    result = jobchange_to(qq,state["job"],True)
    if result[0]:
        skill_trans = skill_text_trans(result[1])
        skill_msg = '\n'.join([f"{skill_trans[i]} ({result[1][i]})" for i in range(len(result[1]))])
        equipment_info = get_equipment_info(result[2])
        equipment_msg = [x["detail"]["name"] for x in equipment_info]
        msgs = ["转职成功\n=========",
        "获得新技能\n=========\n"+skill_msg,
        f"当前装备\n=========【武器】{equipment_msg[0]}\n【头部】{equipment_msg[1]}\n【护具】{equipment_msg[2]}\n【鞋子】{equipment_msg[3]}\n【饰品】{equipment_msg[4]}\n=========\n新装备已同时放入背包~",
        "属性值也获得了加成~"]
        await jobchange.send("转职成功~\n具体信息请看合并消息√",at_sender=True)
        try:
            await send_forward_msg(bot,event,"「雾境」",bot.self_id,msgs)
        except:
            await jobchange.send("发送合并消息失败×\n获得新技能和新装备请另行查看哦~",at_sender=True)



