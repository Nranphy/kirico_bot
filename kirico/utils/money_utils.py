'''Kirico金币管理工具'''

from nonebot import get_driver
from nonebot.log import logger
import os
import json
import random
from .file_utils import check_dir, check_file
from .basic_utils import get_date_and_time




#.env中的金钱变化记录长度设置
try:
    money_change_record_length = int(get_driver().config.money_change_record_length)
except Exception:
    logger.info("[金钱工具]未找到相关配置，已取用默认值。")
    money_change_record_length = 5




def money_change(qq,average:int=0,deviation:int=0,date:str=None,time:str=None,note:str='不知道为什么...') -> list:
    '''
    按某标准及最大偏差增长金钱，可记录金钱变化日期时间与备注,并返回随机出的金钱变化值和存储后的金钱值。
    :param qq: 需要增长金钱的qq号
    :param average: 增长的中间值
    :param deviation: 最大偏差
    :param date: 金钱变化日期（默认为当时日期）
    :param time: 金钱变化时间（默认为当时时间）
    :param note: 金钱变化记录
    :增长的金钱将会在（average ± deviation）范围内取值，当average < deviation时可能取值为负
    :增长值为负且剩余金钱不足时，将返回[0,当前金钱值]，不会做出任何更改。
    '''
    if not date:date = get_date_and_time()[0]
    if not time:time = get_date_and_time()[1]
    json_path = os.getcwd()+f"/kirico/data/money/{qq}.json"
    check_dir(os.getcwd()+f"/kirico/data/money/")
    check_file(json_path)
    with open(json_path,"r") as f: # 仅读取
        try:
            money = json.load(f)
            money_count = money.get("count",0)
            money_change = money.get("change",[])
        except Exception:
            money = dict()
            money_count = 0
            money_change = list()
    
    increase_count = random.randint(average-deviation,average+deviation)
    money_count += increase_count
    if money_count<0:
        return [0,money_count-increase_count]
    money_change.append([date,time,note,increase_count])

    if len(money_change) > money_change_record_length:  # 历史记录长度控制
        money_change = money_change[-money_change_record_length:]

    money["count"] = money_count
    money["change"] = money_change

    with open(json_path,"w+") as f: # 再次打开，以w+模式，便于覆盖数据
        json.dump(money, f)
    return [increase_count,money_count]


def money_inquire(qq) -> list:
    '''
    查询某QQ号的金钱相关信息。
    :param qq: 查询的qq号
    :返回金钱数(int)、金钱改变记录(list)列表.
    '''
    json_path = os.getcwd()+f"/kirico/data/money/{qq}.json"
    check_dir(os.getcwd()+f"/kirico/data/money/")
    check_file(json_path)
    with open(json_path,"r") as f:
        try:
            money = json.load(f)
            money_count = money.get("count",0)
            money_change = money.get("change",[])
        except Exception:
            logger.info("[金钱查询]解析json文件失败，该用户曾未拥有金钱或json格式有误。")
            money = dict()
            money_count = 0
            money_change = list()
    return [money_count, money_change]