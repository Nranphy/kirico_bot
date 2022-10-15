'''Kirico基础开发工具'''


from nonebot import get_driver
from nonebot.log import logger
from nonebot.plugin import get_plugin

from dataclasses import dataclass
from typing import Any, Optional
from pathlib import Path
import time



config = get_driver().config
""".env中机器人配置"""



def get_config(name:str,default:Any=None,config_type:type=None,logger_title:str='获取设置') -> Any:
    '''
    安全的获取所需要的设置项。
    :param name: 需要获得的设置项名称
    :param default: 设置项默认值
    :param config_type: 设置项返回类型，无法转换时将返回默认值，留空则直接返回设置项
    :param logger_title: 未找到设置项时logger标题
    :param logger_msg: 未找到设置项时logger内容
    '''
    if config_type and not isinstance(default, config_type):
        kirico_logger("warning", logger_title, f"设置项 【{name}】 的默认值并非所指定类型，或将导致出错。")
    if hasattr(config,name):
        target_config = config.__getattribute__(name)
        if not config_type:
            return target_config
        else:
            try:
                return config_type(target_config)
            except:
                kirico_logger("warning", logger_title, f"将设置项 【{name}】 转为目标类型时出错，已采用默认值【{default}】。")
                return default
    else:
        kirico_logger("info", logger_title, f"设置项 【{name}】 未找到，已采用默认值【{default}】。")
        return default



def kirico_logger(level:str, title:str, detail:str):
    '''
    在后台输出日志
    :param level: 日志等级，有debug, info, warning, error, critical.
    :param title: 日志标题
    :param detail: 日志内容
    '''
    if level not in ['debug', 'info', 'warning', 'error', 'critical']:
        logger.error("[日志工具] 调用kirico_logger时日志等级设置错误。")
        return
    log = logger.__getattribute__(level)
    log(f"[{title}] {detail}")



from nonebot.plugin import PluginMetadata

@dataclass(eq=False)
class KiricoPluginMetadata(PluginMetadata):
    """KiricoBot用插件元信息"""
    def __post_init__(self):
        kirico_plugin_metadata = {
            "visible": False,
            "default_enable": True
        }
        kirico_plugin_metadata.update(self.extra)

        for k,v in kirico_plugin_metadata.items():
            if not hasattr(self,k):
                setattr(self,k,v)
            else:
                raise ValueError("插件元信息错误，extra中含有已有属性。")


def if_plugin_exists(name:str) -> bool:
    '''
    检查目标插件是否存在
    :param name: 目标插件名称
    :rtype: 若存在则返回对应Plugin，否则返回None
    '''
    return get_plugin(name)



def get_plugin_metadata(name:str) -> Optional[PluginMetadata]:
    '''
    获得目标插件的插件元信息
    :param name: 目标插件名称
    :rtype: 返回目标插件的Metadata，若插件不存在或没有Metadata则返回None.
    '''
    plugin = get_plugin(name)
    if plugin:
        return plugin.metadata
    else:
        return plugin



class KiricoDatetime:
    '''Kirico日期时间类对象'''

    date:str
    '''Kirico日期标准格式，例1970-01-01'''
    time:str
    '''Kirico时间标准格式，例08:30:10'''
    year:int
    month:int
    day:int
    hour:int
    minute:int
    second:int
    timestamp:int
    '''13位时间戳'''

    def __init__(self, timestamp:Optional[int] = None):
        '''获得当前时间的该对象，若有13位timestamp则返回该时间的对象'''
        time_str = self.format_datetime(timestamp)
        self.date = time_str[:10]
        self.time = time_str[11:]
        self.year = int(self.date[:4])
        self.month = int(self.date[5:7])
        self.day = int(self.date[8:])
        self.hour = int(self.time[:2])
        self.minute = int(self.time[3:5])
        self.second = int(self.time[6:])
        self.timestamp = round(time.time()*1000)

    def format_datetime(self, timestamp:Optional[int] = None) -> str:
        '''
        获得标准化日期和时间字符串
        :param timestamp: 13位时间戳
        '''
        if timestamp:
            timestamp /= 1000
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def check_format_date(date:str) -> bool:
    '''检查是否为标准日期格式'''
    if len(date) != 10:
        return False

    year = date[:4]
    month = date[5:7]
    day = date[8:]
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False

    if not (0<int(month)<=12):
        return False
    
    days = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    if int(year) % 4 == 0 and int(year) % 100 != 0 or int(year) % 400 == 0:
        days[2] += 1
    
    if not (0<int(day)<=days[int(month)]):
        return False
    
    return True

