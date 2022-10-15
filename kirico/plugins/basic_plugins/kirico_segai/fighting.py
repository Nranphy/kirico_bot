from typing import Counter, List
from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, GroupMessageEvent, MessageEvent
from nonebot.log import logger
from kirico.utils.message_utils import get_message_at, send_forward_msg
from .utils import attribute_count, elements_react, gain_exp, get_equipment_info, get_skill_info, read_basic, read_honor, read_profession, save_honor, skill_text_trans, role_exist
from .config import kirico_segai_config
from .skill import find_skill

import time
import os
import json
import random



class Fighter:
    def __init__(self,qq):
        self.__dict__.update(read_basic(qq))
        self.__dict__.update(read_profession(qq))
        self.__dict__.update(attribute_count(qq))
        # 将装备特殊属性加入Fighter
        self.race_restrain = Counter()
        for equipment in get_equipment_info(self.equipment):
            if equipment["special"]["skill"]: #装备技能加入self.skill
                self.skill.append(equipment["special"]["skill"])
            self.race_restrain += Counter(equipment["special"]["race_restrain"]) #装备种族克制加入self.race_restrain
        # 筛选出战斗技能，更新self.skill
        skill_info = get_skill_info(self.skill)
        self.skill = list()
        for i in skill_info:
            if i["type"] != 4:
                self.skill.append(i["detail"]["name"])
        return
    
    def attribute(self):
        '''获得最新的Fighter属性值'''
        return {"HP":self.HP,"SP":self.SP,"cAtk":self.cAtk,"dAtk":self.dAtk,"Matk":self.Matk,"Hit":self.Hit,"Cri":self.Cri,"Def":self.Def,"Mdef":self.Mdef,"Flee":self.Flee,"Aspd":self.Aspd}





def fight_between(self:Fighter,ene:Fighter):
    '''
    通用的战斗函数
    :param self: 战斗方之一，通常为自身
    :param ene: 战斗方之二，通常为敌方
    :rtype: [战斗结果int, 战斗信息List[str], 战斗回合数int]
    '''
    def normal_attack(one:Fighter,two:Fighter):
        '''前者普通攻击'''
        # 命中判定
        if one.Hit < two.Flee:
            the_difference = two.Flee - one.Hit
            flee_percent = round(the_difference/100,2)
            if random.random() < flee_percent:
                return [one,two,0,[f"【{one.name}】向【{two.name}】发动了普通攻击，但是并没有命中...\n当前命中率为{1-flee_percent}"]]

        one_equipment_info = get_equipment_info(one.equipment)
        two_equipment_info = get_equipment_info(two.equipment)
        # 获取基础伤害
        the_way = ''
        if one_equipment_info[0]["limit"]["mode"]=='cAtk': 
            dmg = one.cAtk - two.Def
            the_way = " 近程 "
        elif one_equipment_info[0]["limit"]["mode"]=='dAtk': 
            dmg = one.dAtk - two.Def
            the_way = " 远程 "
        elif one_equipment_info[0]["limit"]["mode"]=='Matk': 
            dmg = one.Matk - two.Mdef
            the_way = " 法术 "
        # 伤害兜底
        if dmg<=1: dmg = 1
        # 暴击判定
        if_cri = ''
        if random.randint(0,100) <= one.Cri-100: 
            dmg *= kirico_segai_config("kirico_sagai_fight_critical_times",2)
            if_cri = '触发了暴击，'
        # 元素克制
        if_element_react = ''
        elements_statu = elements_react(one_equipment_info[0]["element"],two_equipment_info[2]["element"])
        if elements_statu==1:
            dmg = int(kirico_segai_config("kirico_sagai_fight_elements_restrain",1.5)*dmg)
            if_element_react = '\n【元素反应】元素克制'
        elif elements_statu==2:
            dmg = int(kirico_segai_config("kirico_sagai_fight_elements_restrain",0.7)*dmg)
            if_element_react = '\n【元素反应】收效甚微'
        # 种族克制
        race_restrain = one.race_restrain.get(two.race,0)
        if_race_restrain = '\n【种族克制】{:+}%'.format(race_restrain) if race_restrain else ''
        dmg = int((100+race_restrain)/100*dmg)
        # 最终处理
        two.HP -= dmg
        fight_msg = [f"【{one.name}】向【{two.name}】发动了{the_way}普通攻击，{if_cri}造成 {dmg} 点伤害...\n======\n【{two.name} HP值】{two.HP}{if_element_react}{if_race_restrain}"]
        return [one,two,0,fight_msg]

    def take_action(one:Fighter,two:Fighter):
        '''前者采取行动'''
        if random.random() <= 0.3+one.Matk/700 and one.skill:
            random_skill = random.choice(one.skill)
            if get_skill_info(random_skill)[0]["consumeSP"] <= one.SP:
                return find_skill(random_skill)(one,two)
            else:
                should_return = normal_attack(one,two)
                should_return[3][0] = f'{one.name} 想要使用技能〖{random_skill}〗，但因为SP不足放弃了...\n=========\n'+should_return[3][0]
                return should_return
        return normal_attack(one,two)
        

    self_skill_info = '\n'.join([f'【{skill_text_trans(x)[0]}】 （{x}）' for x in self.skill])
    enemy_skill_info = '\n'.join([f'【{skill_text_trans(x)[0]}】 （{x}）' for x in ene.skill])
    msgs = [f"""友方
=========
【昵称】 {self.name}
【等级】 {self.level}
======
属性值
（已计算装备和技能加成）
【HP】生命值 {self.HP}
【SP】法力值 {self.SP}
【cAtk】近程攻击 {self.cAtk}
【dAtk】远程攻击 {self.dAtk}
【Matk】法术攻击 {self.Matk}
【Hit】命中 {self.Hit}
【Cri】暴击 {self.Cri}
【Def】物理防御 {self.Def}
【Mdef】法术防御 {self.Mdef}
【Flee】闪避 {self.Flee}
【Aspd】攻击速度 {self.Aspd}
======
主动技能
(包括装备的技能)
{self_skill_info if self_skill_info else "无"}""",
f"""敌方
=========
【昵称】 {ene.name}
【等级】 {ene.level}
======
属性值
（已计算装备和技能加成）
【HP】生命值 {ene.HP}
【SP】法力值 {ene.SP}
【cAtk】近程攻击 {ene.cAtk}
【dAtk】远程攻击 {ene.dAtk}
【Matk】法术攻击 {ene.Matk}
【Hit】命中 {ene.Hit}
【Cri】暴击 {ene.Cri}
【Def】物理防御 {ene.Def}
【Mdef】法术防御 {ene.Mdef}
【Flee】闪避 {ene.Flee}
【Aspd】攻击速度 {ene.Aspd}
======
主动技能
(包括装备的技能)
{enemy_skill_info if enemy_skill_info else "无"}""","战斗开始~\n========="] # 战斗信息
    step = 0 # 记录战斗回数
    turn = 0 # 下次战斗主体，0为友方，1为敌方
    Aspd_bar = 0 # 攻速差值累计条，满一个数值则连续攻击
    while self.HP>0 and ene.HP>0 and step<=500:
        Aspd_difference = self.Aspd - ene.Aspd
        if turn == 0: # 友方操作
            res = take_action(self,ene)
            self,ene = res[:2] # 更新状态
            msgs += res[3] # 更新信息
            turn = 1 # 战斗交替
            step += 1
            Aspd_bar += Aspd_difference
            if self.HP<=0 or ene.HP<=0:
                break
            if res[2]:
                res = res[2] # 处理战斗结果，1为友方胜利，2为敌方胜利，3为平局
                break
        else: # 敌方操作同理
            res = take_action(ene,self)
            ene,self = res[:2]
            msgs += res[3]
            turn = 0
            step += 1
            Aspd_bar += Aspd_difference
            if self.HP<=0 or ene.HP<=0:
                break
            if res[2]: # 结果逻辑与己方操作相反
                if res[2]==1: res=2
                elif res[2]==2: res=1
                else: res=3
                break
        # 速度差控制
        if Aspd_bar >= 2*self.Aspd and turn==1:
            Aspd_bar -= 2*Aspd_difference
            turn = 0
        elif Aspd_bar <= -2*ene.Aspd and turn==0:
            Aspd_bar -= 2*Aspd_difference
            turn = 1
    if self.HP <= 0:
        msgs += ["=========\n友方生命值小于等于0，战斗失败..."]
        res = 2
    elif ene.HP <= 0:
        msgs += ["=========\n敌方生命值小于等于0，战斗胜利~！！"]
        res = 1
    else:
        msgs += ["=========\n由于技能因素或双方战斗超过限制回合，战斗结果为平局×"]
        res = 3
    return [res, msgs, step]
        
        





fight_request = on_command("决斗",aliases={"战斗","挑战"},priority=7,block=True)

@fight_request.handle()
async def fight_prepare(bot:Bot,event:MessageEvent,state:T_State,arg:Message=CommandArg()):
    state["self"] = event.get_user_id()
    if arg:
        state["enemy"] = arg
    else:
        await fight_request.send("请问要和谁决斗呢~？\n可发送at或者QQ号~",at_sender=True)
    
@fight_request.got("enemy")
async def fight_process(bot:Bot,event:MessageEvent,state:T_State):
    state["enemy"] = get_message_at(state["enemy"])
    if len(state["enemy"])>=2:
        await fight_request.send("对于多个决斗目标，只会与系统检测到的第一个进行决斗哦~",at_sender=True)
    if state["enemy"]:
        state["enemy"] = state["enemy"][0]
    else:
        await fight_request.finish("未检测到合法目标...重新试试吧？\n只接受at或者QQ号哦，复制的at信息会无效...",at_sender=True)
    # 判断是否注册
    if not role_exist(state["self"]):
        await fight_request.finish("你还没有注册哦~\n输入【/注册】获取详细~",at_sender=True)
    if not role_exist(state["enemy"]):
        await fight_request.finish("对方还没有注册哦~\n请对方输入【/注册】获取详细哦~",at_sender=True)
    # 判断双方是否为同一人
    if state["self"] == state["enemy"]:
        await fight_request.finish("不能和自己战斗哦~请重新选择目标吧",at_sender=True)
    # 包装Fighter并获取战斗结果
    res = fight_between(Fighter(state["self"]), Fighter(state["enemy"]))
    self_honor = read_honor(state["self"])
    enemy_honor = read_honor(state["enemy"])
    self_profession = read_profession(state["self"])
    enemy_profession = read_profession(state["enemy"])
    ## 处理战斗结果和收获
    self_honor["fight_count"] += 1
    enemy_honor["fight_count"] += 1
    if res[0] == 1:
        self_honor["success_count"] += 1
        self_honor["fight_record"].append([read_basic(state["enemy"])["name"], "发起对", "胜利"])
        enemy_honor["fight_record"].append([read_basic(state["self"])["name"], "收到来自", "失败"])
        exp_increase = gain_exp(state["self"],enemy_profession["level"]*1000,enemy_profession["level"]*400)
        await fight_request.send(f"战斗胜利~\n获得经验值 {exp_increase[0]}\n具体战斗信息请看合并消息哦~",at_sender=True)
    elif res[0] == 2:
        enemy_honor["success_count"] += 1
        self_honor["fight_record"].append([read_basic(state["enemy"])["name"], "发起对", "失败"])
        enemy_honor["fight_record"].append([read_basic(state["self"])["name"], "收到来自", "成功"])
        exp_increase1 = gain_exp(state["self"],enemy_profession["level"]*400,enemy_profession["level"]*200)
        exp_increase2 = gain_exp(state["enemy"],self_profession["level"]*800,self_profession["level"]*400)
        await fight_request.send(f"战斗失败...\n获得经验值 {exp_increase1[0]}，敌方获得经验值 {exp_increase2[0]}\n具体战斗信息请看合并消息哦~",at_sender=True)
    else:
        self_honor["fight_record"].append([read_basic(state["enemy"])["name"], "发起对", "平局"])
        enemy_honor["fight_record"].append([read_basic(state["self"])["name"], "收到来自", "平局"])
        exp_increase1 = gain_exp(state["self"],enemy_profession["level"]*400,enemy_profession["level"]*200)
        exp_increase2 = gain_exp(state["enemy"],self_profession["level"]*400,self_profession["level"]*200)
        await fight_request.send(f"战斗获得平局...\n获得经验值 {exp_increase1[0]}，敌方获得经验值 {exp_increase2[0]}\n具体战斗信息请看合并消息哦~",at_sender=True)
    save_honor(state["self"], self_honor)
    save_honor(state["enemy"], enemy_honor)
    try:
        if len(res[1])>95:
            await send_forward_msg(bot,event,"「雾境」",bot.self_id,res[1][:88]+["======\n战斗过长，中途省略...\n======"]+res[1][-10:])
        else:
            await send_forward_msg(bot,event,"「雾境」",bot.self_id,res[1])
    except:
        await fight_request.send("合并消息发送失败...\n或许是因为战斗太激烈吧×",at_sender=True)