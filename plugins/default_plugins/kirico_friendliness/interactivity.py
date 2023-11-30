from typing import Union
from nonebot import on_regex
from nonebot.typing import T_Handler
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Event

from pathlib import Path
import random
import json

from utils.basic_utils import kirico_logger
from utils.friendliness_utils import KiricoFriendliness
from utils.file_utils import check_cd, set_cd

from .util import interactivity_path, use_nickname, default_interactivity_reply

_interactivity_cd_name = "interactivity"

class Interactivity:
    '''存放交互命令信息'''
    nickname: set = {"kirico", "Kirico","雾子","雾子酱"}

    name:str
    keywords:list[str]
    friendliness:int
    data:dict
    note:str

    def __init__(self, interactivity_path:Union[str, Path]):
        '''创造交互命令信息类
        :param interactivity_path: 交互回复文件路径
        '''
        with open(interactivity_path, "r", encoding="UTF-8-sig") as f:
            resource:dict = json.load(f)
        self.name = resource.get("name", "Unkown")
        self.keywords = resource.get("keywords", ["未定义"])
        self.friendliness = resource.get("friendliness", 0)
        self.data = resource.get("data", {})
        self.note = self.data.get("note", "交互")
    
    def construct_pattern(self) -> str:
        '''根据指令信息返回正则字符串'''
        action = '|'.join(list(self.keywords))
        nickname = '|'.join(list(self.nickname))
        return ".*?("+action+").{0,3}?("+nickname+").*?|.*?("+nickname+").{0,3}?("+action+").*?"



def construct_handler(command:Interactivity) -> T_Handler:
    async def handler(matcher:Matcher, bot:Bot, event:Event):
        qq = event.get_user_id()
        friendliness_info = KiricoFriendliness(qq)

        result = "success"
        # 好感度判定
        if friendliness_info.count < command.friendliness:
            result = "fail"
        # 冷却判定
        if not check_cd(_interactivity_cd_name, qq):
            result = "over"
        
        if result == "success":
            # 重置冷却
            from math import log
            set_cd(_interactivity_cd_name, int(log(command.friendliness)*400), qq) # 冷却公式
            # 记录次数
            friendliness_info.interactivity_recode(command.name)
        # 好感度变化
        result_data = command.data.get(result, {})
        if not result_data.get("reply"):
            result_data["reply"] = default_interactivity_reply[result]
        friendliness_info.change(result_data.get("average", 0), result_data.get("deviation", 0), note=command.note+result_data.get("note", ''))
        await matcher.finish(use_nickname(random.choice(result_data.get("reply",[""])), friendliness_info.nickname), at_sender=True)

    return handler


def create_interactivity_matchers():
    cnt = 0
    for path in interactivity_path.iterdir():
        if not path.name.endswith(".json"):
            continue
        try:
            interactivity_obj = Interactivity(path)

            on_regex(pattern=interactivity_obj.construct_pattern(), priority=20+cnt, block=True, handlers=[construct_handler(interactivity_obj)])
        except:
            kirico_logger("warning", "雾子交互", f"交互配置文件【{path.name}】导入或使用失败，请检查内容格式...")
            continue
        cnt += 1

create_interactivity_matchers()