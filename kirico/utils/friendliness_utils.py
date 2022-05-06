from nonebot import get_driver
from nonebot.log import logger
import os
import json
import random
from kirico.utils.file_utils import check_dir, check_file, get_date_and_time





#.env中的好感度变化记录长度设置
try:
    friendliness_change_record_length = int(get_driver().config.friendliness_change_record_length)
except Exception:
    logger.info("[好感度工具]未找到相关配置，已取用默认值。")
    friendliness_change_record_length = 5




def friendliness_change(qq,average:int=0,deviation:int=10,date:str=None,time:str=None,note:str='不知道为什么...') -> list:
    '''
    按某标准及最大偏差增长好感度，可记录好感度变化日期时间与备注,并返回随机出的好感度变化值和存储后的好感度值。
    :param qq: 需要增长好感度的qq号
    :param average: 增长的中间值
    :param deviation: 最大偏差
    :param date: 好感度变化日期（默认为当时日期）
    :param time: 好感度变化时间（默认为当时时间）
    :param note: 好感度变化记录
    :增长的好感度将会在（average ± deviation）范围内取值，当average < deviation时可能取值为负
    '''
    if not date:date = get_date_and_time()[0]
    if not time:time = get_date_and_time()[1]
    json_path = os.getcwd()+f"/kirico/data/friendliness/{qq}.json"
    check_dir(os.getcwd()+f"/kirico/data/friendliness/")
    check_file(json_path)
    with open(json_path,"r") as f: # 仅读取
        try:
            friendliness = json.load(f)
            friendliness_count = friendliness.get("count",0)
            friendliness_change = friendliness.get("change",[])
        except Exception:
            friendliness = dict()
            friendliness_count = 0
            friendliness_change = list()
    
    increase_count = random.randint(average-deviation,average+deviation)
    friendliness_count += increase_count
    friendliness_change.append([date,time,note,increase_count])

    if len(friendliness_change) > friendliness_change_record_length:  # 历史记录长度控制
        friendliness_change = friendliness_change[-friendliness_change_record_length:]

    friendliness["count"] = friendliness_count
    friendliness["change"] = friendliness_change
    
    with open(json_path,"w+") as f: # 再次打开，以w+模式，便于覆盖数据
        json.dump(friendliness, f)
    return [increase_count,friendliness_count]



def friendliness_inquire(qq) -> list:
    '''
    查询某QQ号的好感度相关信息。
    :param qq: 查询的qq号
    :返回好感度数(int)、好感度改变记录(list)列表.
    '''
    json_path = os.getcwd()+f"/kirico/data/friendliness/{qq}.json"
    check_dir(os.getcwd()+f"/kirico/data/friendliness/")
    check_file(json_path)
    with open(json_path,"r") as f:
        try:
            friendliness = json.load(f)
            friendliness_count = friendliness.get("count",0)
            friendliness_change = friendliness.get("change",[])
        except Exception:
            logger.info("[好感查询]解析json文件失败，该用户曾未拥有好感度或json格式有误。")
            friendliness = dict()
            friendliness_count = 0
            friendliness_change = list()
    return [friendliness_count, friendliness_change]



def get_nickname(qq):
    '''
    对传入的QQ查询别名
    :param qq: 需要查询的qq
    :rtype: 如查询到别名则返回别名str，否则返回空字符串。
    '''
    try:
        with open(os.getcwd()+f"/kirico/data/nickname.json", "r") as f:
            data = json.load(f)
    except:
            data = dict()
    nickname = data.get(qq, '')
    return nickname