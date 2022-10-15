'''Kirico好感度相关工具'''

from typing import Union
import random
from .file_utils import load_data, save_data
from .basic_utils import get_config, KiricoDatetime



friendliness_change_record_length = get_config("friendliness_change_record_length", 5, int)
'''.env中的好感度变化记录长度设置'''

friendliness_data_pathname = "friendliness"


class KiricoFriendliness:
    '''Kirico好感度对象'''

    user_id:int
    nickname:str
    count:int
    change_log:list[int]
    interactivity_count:dict

    now_date:KiricoDatetime

    def __init__(self, user_id: Union[str, int]):
        friendliness_data = load_data(friendliness_data_pathname, user_id)
        self.user_id = str(user_id)
        self.nickname = friendliness_data.get("nickname", '')
        self.count = friendliness_data.get("count", 0)
        self.change_log = friendliness_data.get("change_log", [])
        self.interactivity_count = friendliness_data.get("interactivity_count",{})
        self.now_date = KiricoDatetime()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "nickname": self.nickname,
            "count": self.count,
            "change_log": self.change_log,
            "interactivity_count": self.interactivity_count
        }

    def save_data(self):
        '''保存好感度信息'''
        save_data(friendliness_data_pathname, self.user_id, self.to_dict())

    def change(self, average:int, deviation:int, note:str='不知道为什么...') -> tuple[int]:
        '''
        按某标准及最大偏差增长好感度，可记录好感度变化日期时间与备注。
        :param average: 增长的中间值
        :param deviation: 最大偏差
        :param note: 好感度变化记录
        :rtype: 返回好感度变化值与变化后好感度元组
        :增长的好感度将会在（average ± deviation）范围内取值，当average < deviation时可能取值为负
        '''
        increase_count = random.randint(average-deviation,average+deviation)
        self.count += increase_count

        self.change_log.append([self.now_date.date, self.now_date.time, note, increase_count])
        if len(self.change_log) > friendliness_change_record_length:
            self.change_log = self.change_log[-friendliness_change_record_length:]
        self.save_data()
        return (increase_count, self.count)

    def set_nickname(self, nickname:str):
        '''设定nickname'''
        self.nickname = nickname
        self.save_data()

    def interactivity_recode(self, action:str):
        '''增加一次指定交互次数'''
        cnt = self.interactivity_count.get(action, 0)
        self.interactivity_count[action] = cnt+1
        self.save_data()