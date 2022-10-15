from kirico.utils.basic_utils import KiricoDatetime
from kirico.utils.file_utils import load_data, save_data

from typing import Union


_kirico_sign_in_data_pathname = "sign_in"


class KiricoSigninData:

    qq:str
    total_days:int
    max_continuous_days:int
    last_date:str
    complement:int
    sign_in_status:list[int]
    '''每月签到概况，第一位为上月最后一天，值均为当天连续签到数'''

    now_date:KiricoDatetime

    def __init__(self, qq:Union[str, int]):
        self.now_date = KiricoDatetime()
        self.qq = str(qq)
        user_data = {
            "qq": str(qq),
            "total_days": 0,
            "max_continuous_days": 0,
            "last_date": '0000-00-00',
            "complement": 0,
            "sign_in_status": [0]
        }
        user_data.update(self.read_data())
        for k,v in user_data.items():
            setattr(self, k, v)
        self._current_month_calendar()
        self.save_data()
        
    def _current_month_calendar(self):
        '''为对象更新月历，若同月则不更新'''
        if int(self.last_date[:4]) == self.now_date.year and int(self.last_date[5:7]) == self.now_date.month:
            return # 无需更新
        # 获得每月天数
        days = [0,31,28,31,30,31,30,31,31,30,31,30,31]
        if self.now_date.year % 4 == 0 and self.now_date.year % 100 != 0 or self.now_date.year % 400 == 0:
            days[2] += 1
        # 更新月历
        self.sign_in_status = [self.sign_in_status[-1]] + [0]*(days[self.now_date.month])
        
        
    def to_dict(self) -> dict:
        '''将签到信息包装成字典'''
        return {
            "qq": self.qq,
            "total_days": self.total_days,
            "max_continuous_days": self.max_continuous_days,
            "last_date": self.last_date,
            "complement": self.complement,
            "sign_in_status": self.sign_in_status
        }

    def save_data(self):
        '''保存签到信息'''
        save_data(_kirico_sign_in_data_pathname, self.qq, self.to_dict())

    def read_data(self) -> dict:
        '''获取原有签到信息，若不存在则返回空字典'''
        return load_data(_kirico_sign_in_data_pathname, self.qq)


    def sign(self) -> bool:
        '''进行签到，返回签到是否成功'''
        # 重复签到拒绝
        if self.last_date == self.now_date.date:
            return False
        # 记录签到操作
        self.total_days += 1
        self.sign_in_status[self.now_date.day] = self.sign_in_status[self.now_date.day-1] + 1
        self.max_continuous_days = max(self.max_continuous_days, self.sign_in_status[self.now_date.day])
        self.last_date = self.now_date.date
        self.save_data()
        return True

    def complement_sign(self, day:int = 0) -> bool:
        '''
        进行一次补签，只能补签当前月份的日期，返回是否成功
        :param day: 目标日期，若未给予，则自动指定上一次未签到处（不包括今天）
        '''
        today = self.now_date.day
        if not day:
            for i in range(today-1, 0, -1):
                if not self.sign_in_status[i]:
                    day = i
                    break
        
        if day<=0 or day >= today:
            return False
        
        if self.sign_in_status[day]:
            return False

        self.total_days += 1
        self.complement += 1
        if self.last_date < self.now_date.date:
            self.last_date = self.now_date.date
        self.sign_in_status[day] = self.sign_in_status[day-1] + 1
        for i in range(day, today+1):
            if self.sign_in_status[i]:
                self.sign_in_status[i] = self.sign_in_status[i-1] + 1
                self.max_continuous_days = max(self.max_continuous_days, self.sign_in_status[i])
            else:
                break
        self.save_data()
        return True

    def today_have_sign(self) -> bool:
        '''返回今日是否签到'''
        return bool(self.sign_in_status[self.now_date.day])

    def today_continuous_days(self) -> int:
        '''返回今日或昨日连续签到数'''
        res = self.sign_in_status[self.now_date.day]
        if res:
            return res
        else:
            return self.sign_in_status[self.now_date.day-1]