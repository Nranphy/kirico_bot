from typing import Any
from nonebot import get_driver
from nonebot.log import logger


config = get_driver().config

def get_config(name:str,default:Any=None,logger_title:str='获取设置',logger_msg:str='') -> Any:
    '''
    安全的获取所需要的设置项。
    :param name: 需要获得的设置项名称
    :param default: 设置项默认值
    :param logger_title: 未找到设置项时logger标题
    :param logger_msg: 未找到设置项时logger内容
    '''
    if hasattr(config,name):
        return config.__getattribute__(name)
    else:
        if not logger_msg:
            logger_msg = f"设置项 【{name}】 未找到，已采用默认值【{default}】。"
        logger.info(f"[{logger_title}] {logger_msg}")
        return default