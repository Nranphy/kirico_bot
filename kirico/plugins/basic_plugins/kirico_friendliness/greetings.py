from typing import Union
from nonebot import on_regex
from nonebot.typing import T_Handler
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Event

from pathlib import Path
import random
import json

from kirico.utils.basic_utils import kirico_logger
from kirico.utils.friendliness_utils import KiricoFriendliness
from kirico.utils.file_utils import set_cd, check_cd

from .util import greeting_path, use_nickname



_greeting_cd_name = "greeting_cd_name"
'''问候与自动问候共用CD名'''


class Greeting:
    '''存放问候命令信息'''
    nickname: set = {"kirico", "Kirico","雾子","雾子酱"}

    name:str
    keywords:list[str]
    overgreeting:list[str]
    auto:dict
    data:list[dict]

    def __init__(self,greeting_path:Union[str, Path]):
        '''创造问候命令信息类
        :param greeting_path: 问候回复文件路径
        '''
        with open(greeting_path, "r", encoding="UTF-8-sig") as f:
            resource:dict = json.load(f)
        self.name = resource.get("name", "Unkown")
        self.keywords = resource.get("keywords", ["未定义"])
        self.overgreeting = resource.get("overgreeting", [])
        self.auto = resource.get("auto", {})
        self.data = resource.get("data", [])
    
    def construct_greeting_pattern(self) -> str:
        '''返回问候触发所用正则字符串'''
        greet = '|'.join(list(self.keywords))
        nickname = '|'.join(list(self.nickname))
        return ".*?("+greet+").{0,3}?("+nickname+").*?|.*?("+nickname+").{0,3}?("+greet+").*?"
    
    def construct_auto_pattern(self) -> str:
        '''返回自动问候触发所用正则字符串'''
        greet = '|'.join(list(self.keywords))
        return ".*?("+greet+").{0,3}?.*?"



def construct_greeting_handler(greeting:Greeting) -> T_Handler:
    '''获得指定Greeting的问候处理函数'''
    async def handler(matcher:Matcher, event:Event):
        qq = event.get_user_id()
        friendliness_info = KiricoFriendliness(qq)
        # 冷却判定
        if not check_cd(_greeting_cd_name):
            await matcher.finish(use_nickname(random.choice(greeting.overgreeting), friendliness_info.nickname), at_sender=True)
        else:
            set_cd(_greeting_cd_name, 7200, qq)
        # 依次判断时间段，符合则进行操作
        for data in greeting.data:
            if (not data.get("time", []) or data.get("time")[0]<= friendliness_info.now_date.hour <data.get("time")[1]):
                friendliness_data = data.get("friendliness_data",{})
                friendliness_info.change(friendliness_data.get("average", 0), friendliness_data.get("deviation", 0), friendliness_data.get("note", "问候"))
                await matcher.finish(use_nickname(random.choice(data.get("words",[""])), friendliness_info.nickname), at_sender=True)
    
    return handler

def construct_auto_handler(greeting:Greeting) -> T_Handler:
    '''获得指定Greeting的自动问候处理函数'''
    async def handler(matcher:Matcher, event:Event):
        qq = event.get_user_id()
        friendliness_info = KiricoFriendliness(qq)
        # 时间判定
        if not (greeting.auto.get("time", [0,0])[0] <= friendliness_info.now_date.hour < greeting.auto.get("time", [0,0])[1]):
            await matcher.finish()
        # 好感判定
        if friendliness_info.count < greeting.auto.get("friendliness", 0):
            await matcher.finish()
        # 概率判定
        if random.random() < 0.7:
            await matcher.finish()
        # 冷却判定
        if not check_cd(_greeting_cd_name):
            await matcher.finish(use_nickname(random.choice(greeting.overgreeting), friendliness_info.nickname), at_sender=True)
        else:
            set_cd(_greeting_cd_name, 7200, qq)

        # 进行回复
        await matcher.finish(use_nickname(random.choice(greeting.auto.get("reply",[""])), friendliness_info.nickname), at_sender=True)
    
    return handler
        

def create_greet_matchers():
    for path in greeting_path.iterdir():
        if not path.name.endswith(".json"):
            continue
        try:
            greeting_obj = Greeting(path)
            on_regex(pattern=greeting_obj.construct_greeting_pattern(), priority=7, block=True, handlers=[construct_greeting_handler(greeting_obj)])
            on_regex(pattern=greeting_obj.construct_auto_pattern(), priority=15, block=True, handlers=[construct_auto_handler(greeting_obj)])
        except:
            kirico_logger("warning", "雾子问候", f"问候配置文件【{path.name}】导入或使用失败，请检查内容格式...")
            continue

create_greet_matchers()