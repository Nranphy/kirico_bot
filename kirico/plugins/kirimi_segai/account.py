from nonebot import on_command, get_bot, get_driver, on_startswith
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent
from nonebot.log import logger
from kirico.utils.message_utils import send_forward_msg
from kirico.utils.file_utils import check_dir, check_file, rm_path
from .utils import get_equipment_info, get_skill_info, job_text_trans, race_text_format, race_text_trans, read_bag, read_basic, read_honor, read_profession, read_statu, save_bag, save_honor, role_exist, save_statu,save_basic,save_profession,get_race_info,attribute_count, skill_text_trans
import time
import os
import json
import random
import re


# 获取注册表单
register_information = on_command("register", aliases={"注册","注册账号","账号注册","帐号注册","注册帐号"}, priority=9, block=True)


@register_information.handle()
async def register_prepare(bot:Bot, event:GroupMessageEvent, state:T_State=State()):
    qq = event.get_user_id()
    msgs = ['已注册用户需要先【/删除帐号】才可以重新注册哦~','====分割线===='] if role_exist(qq) else []
    msgs += ['【前排提醒】\n本小游戏的初衷为制作一个“文字RPG游戏”，并非单纯依凭机器人做群聊小游戏。\n所以，本游戏会尽力避免图片出现，包括但不限于长文本图片、游戏物品图片、角色操作图片。\n敬请谅解。\n=========',
'请按以下要求复制、填写注册信息并直接发送哦~',
'请勿删除或更改下面信息中的“中括号”和其中内容，填写内容紧贴“】”后√',
'若有不了解的选项或细节，请输入【/雾境 xxx】查找相关词条~',
'====分割线====',
'''【雾境注册】(请保证以此行开头)
=========
基本信息除种族外均不会对游戏数值产生影响。
【昵称】（汉字、英语、数字和下划线，请仔细考虑哦~）
【年龄】（合理的整数）
【性别】（可选 男|女|扶她|无性|其他）
【身高】（整数，单位cm,在合理范围内）
【体重】（整数，单位kg,在合理范围内）
【种族】（影响初始固定属性点、后续职业和技能。可选 人类|精灵|龙裔|半精灵|半兽人|恶魔）
=========
素质值均为整数。
初始可用属性点为20，请保证分配点数不大于20.若总和小于20，多余点数将会保留。
【Str】（力量，影响近距离物理攻击力）
【Agi】（敏捷，影响攻击速度、闪避率、物理防御力）
【Vit】（体质，影响物理防御力、魔法防御力、HP值）
【Int】（智力，影响魔法攻击力、咏唱时间、魔法防御力、SP值）
【Dex】（灵巧，影响远距离物理攻击力、命中率、咏唱时间、魔法攻击力）
【Luk】（幸运，影响暴击率、命中率、物理攻击力、魔法攻击力、闪避率）''']
    await register_information.send("详细说明请看合并消息哦~",at_sender=True)
    try:
        await send_forward_msg(bot,event,"「雾境」",bot.self_id,msgs)
    except:await register_information.finish("合并消息发送失败...稍后再试吧×")
    await register_information.finish()



# 处理注册信息
register = on_startswith("【雾境注册】",priority=9,block=True)

@register.handle()
async def register_process(bot:Bot, event:GroupMessageEvent):
    # 检测是否曾注册
    qq = event.get_user_id()
    main_path = os.getcwd()+f"/kirico/data/kirico_segai/{qq}/"
    if role_exist(qq):
        await register.finish("你已经注册过了哦~\n若想重新注册，请先【/删除账号】√",at_sender=True)
    
    # 处理注册信息
    txt = event.get_plaintext()
    basic_dic = {"name":"无名氏","age":"未知","sexual":"未知","stature":"未知","weight":"未知"}
    statu_dic = {"Str":0,"Agi":0,"Vit":0,"Int":0,"Dex":0,"Luk":0,"point":0}
    profession_dic = {"level":1,"exp":0,"needexp":7260,"job":"Novice","race":"Unkowned","skill":[],"equipment":['0','None','None','None','None']}
    bag_dic = {"item":{},"skill":[],"equipment":['0','1','2','3']}
    honor_dic = {"fight_count":0,"success_count":0,"beat_boss":[],"fight_record":[],"title":[]}
    
    try:basic_dic["name"] = re.search("(?<=【昵称】)[\u4E00-\u9FA5A-Za-z0-9_]+",txt,re.U).group() 
    except:pass
    try:basic_dic["age"] = re.search("(?<=【年龄】)\+?[1-9][0-9]{0,4}",txt,re.U).group()
    except:pass
    try:basic_dic["sexual"] = re.search("(?<=【性别】)(男|女|扶她|无性|其他)",txt,re.U).group()
    except:pass
    try:basic_dic["stature"] = re.search("(?<=【身高】)\+?[1-9][0-9]{1,2}",txt,re.U).group()
    except:pass
    try:basic_dic["weight"] = re.search("(?<=【体重】)\+?[1-9][0-9]{1,2}",txt,re.U).group()
    except:pass
    try:profession_dic["race"] = re.search("(?<=【种族】)(人类|精灵|龙裔|半精灵|半兽人|恶魔)",txt,re.U).group()
    except:pass

    try:statu_dic["Str"] = int(re.search("(?<=【Str】)\+?[0-9]{1,2}",txt,re.U).group())
    except:pass
    try:statu_dic["Agi"] = int(re.search("(?<=【Agi】)\+?[0-9]{1,2}",txt,re.U).group())
    except:pass
    try:statu_dic["Vit"] = int(re.search("(?<=【Vit】)\+?[0-9]{1,2}",txt,re.U).group())
    except:pass
    try:statu_dic["Int"] = int(re.search("(?<=【Int】)\+?[0-9]{1,2}",txt,re.U).group())
    except:pass
    try:statu_dic["Dex"] = int(re.search("(?<=【Dex】)\+?[0-9]{1,2}",txt,re.U).group())
    except:pass
    try:statu_dic["Luk"] = int(re.search("(?<=【Luk】)\+?[0-9]{1,2}",txt,re.U).group())
    except:pass
    last_point = 20-sum(statu_dic.values())
    if last_point<0:
        await register.finish("点数分配错误×\n请重新提交！",at_sender=True)
    else:
        statu_dic["point"] = last_point
    race_file = get_race_info(profession_dic["race"])
    race_status_dic = race_file["initial_status"]
    race_equipments = race_file["initial_equipments"]
    msgs = ["注册成功！！你的注册信息如下~","如有选项并非期望值，请检查输入格式并输入【/删除账号】后重新发送注册~","====分割线====",
f'''【雾境注册】
=========
【昵称】{basic_dic["name"]}
【年龄】{basic_dic["age"]}
【性别】{basic_dic["sexual"]}
【身高】{basic_dic["stature"]}
【体重】{basic_dic["weight"]}
【种族】{profession_dic["race"]}
=========
素质值（前者为种族初始值，后者为加点）
【Str】{race_status_dic["Str"]}+{statu_dic["Str"]}
【Agi】{race_status_dic["Agi"]}+{statu_dic["Agi"]}
【Vit】{race_status_dic["Vit"]}+{statu_dic["Vit"]}
【Int】{race_status_dic["Int"]}+{statu_dic["Int"]}
【Dex】{race_status_dic["Dex"]}+{statu_dic["Dex"]}
【Luk】{race_status_dic["Luk"]}+{statu_dic["Luk"]}
多余点数已保留：{statu_dic["point"]}''']
    # 此时才把初始值加上去
    for statu,initial in race_status_dic.items():
        statu_dic[statu] += initial
    profession_dic["equipment"] = race_equipments
    profession_dic["race"] = race_text_format(profession_dic["race"])
    if save_basic(qq,basic_dic) and save_statu(qq,statu_dic) and save_profession(qq,profession_dic) and save_bag(qq,bag_dic) and save_honor(qq,honor_dic):
        pass
    else:
        rm_path(os.getcwd()+f"/kirico/data/kirico_segai/{event.get_user_id()}/")
        await register.finish("文件读写错误×\n请稍后再试哦...",at_sender=True)
    
    try:
        await register.send("注册成功~详细说明请看合并消息哦~",at_sender=True)
        await send_forward_msg(bot,event,"「雾境」",bot.self_id,msgs)
    except:await register.finish("合并消息发送失败...请另行检查个人信息×")
    await register.finish()




# 获取账号信息
information = on_command("账号信息", aliases={"查询帐号","查询账号","帐号信息","查看帐号","查看账号","账号查询","帐号查询"}, priority=9, block=True)

@information.handle()
async def get_information(bot:Bot, event:GroupMessageEvent):
    # 检测是否未注册
    qq = event.get_user_id()
    if not role_exist(qq):
        await register.finish("你还未注册哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    # 读取用户存档
    attribute = attribute_count(qq)
    basic = read_basic(qq)
    statu = read_statu(qq)
    profession = read_profession(qq)
    bag = read_bag(qq)
    honor = read_honor(qq)
    # 部分数据处理
    equipment_info = get_equipment_info(profession["equipment"])
    bag_equipment_info = get_equipment_info(bag["equipment"])
    bag_equipment_info_name = "\n".join([equip.get("detail",{}).get("name","未知×")+f"（{equip.get('item','None')}）" for equip in bag_equipment_info])
    bag_skill_info = get_skill_info(bag["skill"])
    bag_skill_info_name = "\n".join([skill.get("detail",{}).get("transname","未知×")+f"（{skill.get('detail',{}).get('name','None')}）" for skill in bag_skill_info])
    pve_record = '\n'.join([f"<{x[0]}> 最小战斗轮数 {x[1]} |最早挑战等级 {x[2]}" for x in honor["beat_boss"]])
    pvp_record = '\n'.join([f"{x[1]}【{x[0]}】的挑战，战斗【{x[2]}】" for x in reversed(honor["fight_record"])])
    skill_record = '\n'.join([f"【{skill_text_trans(x)[0]}】 （{x}）" for x in profession['skill']])
    msgs = [
'你的账号信息如下哦~',
f'''基本信息
=========
【名称】{basic["name"]}
【年龄】{basic["age"]}
【性别】{basic["sexual"]}
【身高/体重】{basic["stature"]}/{basic["weight"]}
===
【等级】{profession["level"]}
【当前经验】{profession["exp"]}
【升级所需经验】{profession["needexp"]}
【种族】{race_text_trans(profession["race"])} （{profession["race"]}）
【职业】{job_text_trans(profession["job"])} （{profession["job"]}）
=========''',
f'''成就信息
=========
【战斗总数】{honor["fight_count"]}
【胜利数】{honor["success_count"]}
===
【PVE记录】
{pve_record}
===
【PVP记录】
{pvp_record}
=========''',
f'''素质点信息
=========
【Str】{statu["Str"]}
【Agi】{statu["Agi"]}
【Vit】{statu["Vit"]}
【Int】{statu["Int"]}
【Dex】{statu["Dex"]}
【Luk】{statu["Luk"]}
【剩余点数】{statu["point"]}
=========''',
f'''属性信息
=========
【HP】生命值{attribute["HP"]}
【SP】法力值{attribute["SP"]}
【cAtk】近程攻击{attribute["cAtk"]}
【dAtk】远程攻击{attribute["dAtk"]}
【Matk】法术攻击{attribute["Matk"]}
【Hit】命中{attribute["Hit"]}
【Cri】暴击{attribute["Cri"]}
【Def】物理防御{attribute["Def"]}
【Mdef】法术防御{attribute["Mdef"]}
【Flee】闪避{attribute["Flee"]}
【Aspd】攻击速度{attribute["Aspd"]}
=========''',
f'''装备信息
=========
（括号内为装备编号）
【武器】{equipment_info[0].get("detail",{}).get("name","空")}（{profession["equipment"][0]}）
【头部】{equipment_info[1].get("detail",{}).get("name","空")}（{profession["equipment"][1]}）
【护具】{equipment_info[2].get("detail",{}).get("name","空")}（{profession["equipment"][2]}）
【鞋子】{equipment_info[3].get("detail",{}).get("name","空")}（{profession["equipment"][3]}）
【饰品】{equipment_info[4].get("detail",{}).get("name","空")}（{profession["equipment"][4]}）
=========''',
f'''技能信息（不包含装备技能）
=========
（括号内为技能英文名）
{skill_record}
=========''',
f'''背包信息
=========
【拥有装备】\n（括号内为装备编号，使用[/更换装备 xxx]来更换装备。）\n'''+bag_equipment_info_name+"\n=========\n【拥有技能】\n（括号内为技能编号及名称，使用[/添加技能 xxx]来装备技能。）\n"+bag_skill_info_name
    ]
    await information.send("查询成功~\n你的账号信息已放入以下合并消息~",at_sender=True)
    try:
        await send_forward_msg(bot,event,"「雾境」",bot.self_id,msgs)
    except:await information.finish("发送合并消息失败...\n请稍后再试×",at_sender=True)
    await information.finish()



# 删除账号

delete = on_command("删除账号",aliases={"删除帐号","帐号删除","账号删除"},priority=9,block=True)


@delete.handle()
async def delete_account(bot:Bot,event:GroupMessageEvent,state:T_State=State()):
    qq = event.get_user_id()
    if not role_exist(qq):
        await delete.finish("你还未拥有角色哦~\n请输入【/注册账号】了解详细吧~",at_sender=True)
    string = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    state["random_str"] = ''.join([random.choice(string) for x in range(5)])
    await delete.send(f"诶...？要删除账号吗？\n请输入【{state['random_str']}】进行确认...",at_sender=True)

@delete.got("print")
async def delete_account_success(bot:Bot,event:GroupMessageEvent,state:T_State=State()):
    if state["random_str"] == str(state["print"]):
        main_path = os.getcwd()+f"/kirico/data/kirico_segai/{event.get_user_id()}/"
        rm_path(main_path)
        await delete.finish("删除账号成功...\n雾子...还能与你再见吗？",at_sender=True)
    else:
        await delete.finish("验证输入出错×\n删除账号失败...",at_sender=True)