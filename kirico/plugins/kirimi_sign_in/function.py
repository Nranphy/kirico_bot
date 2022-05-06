import json
import time
import os
from nonebot.log import logger
from kirico.utils.file_utils import check_dir, check_file
from kirico.utils.money_utils import money_change
from kirico.utils.friendliness_utils import friendliness_change


async def sign_in(qq):
    '''
    签到函数
    :param qq: 签到的QQ号
    :签到成功返回本次签到日期、时间、总次数、连续次数、好感度变化、金钱变化，失败返回False.
    '''
    json_path = os.getcwd()+f"/kirico/data/sign_in/{qq}.json"
    check_dir(os.getcwd()+f"/kirico/data/sign_in/")
    check_file(json_path)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    date_str = time_str[:10]
    time_str = time_str[11:]
    #判断满足签到条件，并对签到统计做出变化。
    with open(json_path,"r") as f:
        try:
            information = json.load(f)
        except Exception:
            information = dict()
    
    last_date = information.get("date","0-0-0")
    if last_date == date_str: #重复签到而被拒绝
        return False
    else: #更改数据，且无论json是否原为空
        information["date"] = date_str
        information["time"] = time_str
        information["total"] = information.get("total",0) + 1
        if if_date_continue(last_date,date_str):
            information["continue"] += 1
        else:
            information["continue"] = 1
    with open(json_path,"w") as f:
        json.dump(information,f)
    #好感度变化
    friendliness = friendliness_change(qq,30,10,date_str,time_str,"签到成功，获得好感值")
    #金币变化
    money = money_change(qq,2000,1500,date_str,time_str,"签到成功，获得雾团子")
    return [information["date"],information["time"],information["total"],information["continue"],friendliness,money]


async def sign_in_inquire(qq) -> list:
    '''
    签到查询函数
    :param qq: 查询签到的QQ号
    :查询成功返回[今日是否签到布尔值、上次签到日期、时间、总次数、连续次数]，失败返回False(可能因为无签到记录或json格式错误).
    '''
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    date_str = time_str[:10]

    json_path = os.getcwd()+f"/kirico/data/sign_in/{qq}.json"
    check_dir(os.getcwd()+f"/kirico/data/sign_in/")
    check_file(json_path)
    with open(json_path,"r") as f:
        try:
            information = json.load(f)
        except Exception:
            logger.info("[签到查询]解析json文件失败，该用户曾未签到或json格式有误。")
            return False
    last_date = information.get("date","无日期记录")
    last_time = information.get("time","无时间记录")
    last_total = information.get("total","无签到记录")
    last_continue = information.get("continue",0)
    
    return [date_str == last_date, last_date, last_time, last_total, last_continue]















def if_date_continue(old_date:str, new_date:str) -> bool:
    '''
    简单的判断两个日期是否连续，日期格式是“xx-xx-xx”，且数字正常且正确，且前一日期更早。
    '''
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    old_date = [int(x) for x in old_date.split("-")]
    new_date = [int(x) for x in new_date.split("-")]
    if new_date[0]%4==0 and new_date[0]%100!=0 or new_date[0]%400 ==0:
        days[1] += 1
    if old_date[2]+1 > days[old_date[1]-1]:
        old_date[2] = 1
        old_date[1] += 1
        if old_date[1] > 12:
            old_date[1] = 1
            old_date[0] += 1
    else:
        old_date[2] += 1
    return old_date == new_date