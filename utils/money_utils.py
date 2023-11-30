'''Kirico金币相关工具'''

from typing import Union
import random
from .file_utils import load_data, save_data
from .basic_utils import get_config, KiricoDatetime



money_change_record_length = get_config("money_change_record_length", 5, int)
'''.env中的金币变化记录长度设置'''

money_data_pathname = "money"


class KiricoMoney:
    '''Kirico雾团子金币对象'''

    user_id:int
    count:int
    change_log:list[int]

    now_date:KiricoDatetime

    def __init__(self, user_id: Union[str, int]):
        money_data = load_data(money_data_pathname, user_id)
        self.user_id = str(user_id)
        self.count = money_data.get("count", 0)
        self.change_log = money_data.get("change_log", [])
        self.now_date = KiricoDatetime()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "count": self.count,
            "change_log": self.change_log
        }

    def save_data(self):
        '''保存金币信息'''
        save_data(money_data_pathname, self.user_id, self.to_dict())

    def change(self, average:int, deviation:int, note:str='不知道为什么...') -> tuple[int]:
        '''
        按某标准及最大偏差改变金币，可记录金币变化日期时间与备注。
        :param average: 增长的中间值
        :param deviation: 最大偏差
        :param note: 金币变化记录
        :rtype: 返回金币变化值与变化后金币元组
        :增长的金币将会在（average ± deviation）范围内取值，当average < deviation时可能取值为负
        '''
        increase_count = random.randint(average-deviation,average+deviation)
        self.count += increase_count

        self.change_log.append([self.now_date.date, self.now_date.time, note, increase_count])
        if len(self.change_log) > money_change_record_length:
            self.change_log = self.change_log[-money_change_record_length:]
        self.save_data()
        return (increase_count, self.count)