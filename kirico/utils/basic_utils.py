'''Kirico基础开发工具'''


from dataclasses import dataclass, field
from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseModel
from typing import Optional, Type, Dict, Any
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
    def __post__init__(self):
        for k,v in self.extra.items():
            if not hasattr(self,k):
                setattr(self,k,v)
            else:
                raise ValueError("插件元信息错误，extra中含有已有属性。")



def get_date_and_time() -> list[str]:
    '''
    返回Kirico标准化当前日期与时间。
    :rtype: 返回含有标准化日期(str)和时间(str)的列表。
    '''
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    date_str = time_str[:10]
    time_str = time_str[11:]
    return [date_str, time_str]