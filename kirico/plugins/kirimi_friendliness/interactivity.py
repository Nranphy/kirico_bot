from nonebot import on_command, get_bot, get_driver, on_regex
from nonebot.typing import T_State, T_Handler
from nonebot.params import State
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
from kirico.utils.friendliness_utils import friendliness_inquire, friendliness_change, get_nickname
from kirico.utils.file_utils import get_date_and_time, check_dir, check_file
from kirico.utils.config_utils import get_config

from .words_data import words

import random
import os
import json



class Interactivity:
    '''存放交互命令信息'''
    def __init__(self,keywords:set, alia:str, trans:str, friendliness:int, increase:int, deviation:int, nickname: set = get_config("nickname",{"雾子"})):
        '''创造交互命令信息类
        :param keywords: 触发交互关键词
        :param alia: 交互行为别名
        :param trans: 交互行为标准翻译名
        :param friendliness: 交互所需好感度
        :param increase: 成功时增长好感度均值
        :param deviation: 成功时增长好感度浮动量
        :param nickname: 机器人名，默认为.env中所设置的
        '''
        self.keywords = keywords
        self.alia = alia
        self.trans = trans
        self.friendliness = friendliness
        self.increase = increase
        self.deviation = deviation
        self.nickname = nickname
    
    def construct_pattern(self) -> str:
        '''根据指令信息返回正则字符串'''
        action = '|'.join(list(self.keywords))
        nickname = '|'.join(list(self.nickname))
        return ".*?("+action+").{0,2}?("+nickname+").*?|.*?("+nickname+").{0,2}?("+action+").*?"


commands = [
    Interactivity({"摸","摸摸","摸头"},"pet","摸摸",50,15,5),
    Interactivity({"贴","贴贴"},"tete","贴贴",100,20,5),
    Interactivity({"抱","抱抱"},"hug","抱抱",100,20,5),
    Interactivity({"举","举起","举高"},"lift","举起",10,15,10),
    Interactivity({"揉","揉揉"},"rua","揉揉",100,20,5),
    Interactivity({"捏捏","捏","掐"},"nip","捏捏",80,20,5),
    Interactivity({"蹭","蹭蹭"},"rub","蹭蹭",100,20,5),
    Interactivity({"亲","亲亲","啾","啾啾","mua","kiss"},"kiss","亲亲",100,20,10),
    Interactivity({"肛","啪","透","草","超市","茶包","炒饭","铜丝","橄榄","中出","爆炒"},"sex","啪啪",3000,0,150),
    Interactivity({"爬","爪巴","滚","傻逼","弱智","脑残","脑瘫","脑弹","智障","废物","fw","垃圾","烧鸡","烧杯"},"dirty","骂",0,-50,50)
]


def create_matchers():
    def construct_handler(command:Interactivity) -> T_Handler:
        async def handler(matcher:Matcher, bot:Bot, event:Event):
            qq = event.get_user_id()
            friendliness = friendliness_inquire(qq)[0]
            nickname = get_nickname(qq)
            date_time = get_date_and_time()
            # 好感度判定
            if friendliness < command.friendliness:
                friendliness_change(qq,5,5,note=f"想要{command.trans}雾子，但是被拒绝了...")
                await matcher.finish(random.choice(words.get(command.alia+"_fail",words.get("fail",["插件怎么会没有默认拒绝语呢？..."]))).replace("[NICK]",nickname).replace("[NICKS]",nickname+"的"), at_sender=True)
            # 冷却判定
            cd_path = os.getcwd()+f"/data/interactivity_cache/{qq}.json"
            check_dir(os.getcwd()+"/data/interactivity_cache/")
            check_file(cd_path)
            try:
                with open(cd_path,"r") as f:
                    cd_data = json.load(f)
            except:
                cd_data = {}
            last = cd_data.get(command.alia,["0000-00-00","00:00:00"])
            if last[0]==date_time[1] and last[1][:2] == date_time[1][:2] and int(last[1][3:5])-int(cd_data[1][3:5])<10:
                await matcher.finish(random.choice(words.get(command.alia+"_over",words.get("over",["插件怎么会没有默认冷却回复语呢？..."]))).replace("[NICK]",nickname).replace("[NICKS]",nickname+"的"), at_sender=True)
            # 各项判定已通过
            # 好感度增长
            friendliness_change(qq,command.increase,command.deviation,note=f"{command.trans}雾子~好感度增加 ")
            # 重置冷却
            cd_data[command.alia] = date_time
            try:
                with open(cd_path,"w") as f:
                    json.dump(cd_data,f)
            except:
                logger.info("[交互系统] 重置交互冷却失败...")
            # 记录次数
            record_path = os.getcwd()+f"/kirico/data/friendliness/interactivity/{qq}.json"
            check_dir(os.getcwd()+"/kirico/data/friendliness/interactivity/")
            check_file(record_path)
            try:
                with open(record_path,"r") as f:
                    record_data = json.load(f)
            except:
                record_data = dict()
            record_data[command.alia] = record_data.get(command.alia,0) + 1
            try:
                with open(record_path,"w") as f:
                    json.dump(record_data,f)
            except:
                await matcher.send("[交互系统] 交互记录更新失败...",at_sender=True)
            await matcher.finish(random.choice(words.get(command.alia,["这个交互怎么没有设定回复语呢？..."])).replace("[NICK]",nickname).replace("[NICKS]",nickname+"的"), at_sender=True)

        return handler
    
    for command in commands:
        on_regex(pattern=command.construct_pattern(),priority=7,block=True).append_handler(construct_handler(command))

create_matchers()

