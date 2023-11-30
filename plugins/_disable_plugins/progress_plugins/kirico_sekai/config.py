from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
from kirico.utils.file_utils import check_dir, check_file




main_config = get_driver().config

# kirico_sagai_fight_critical_times #暴击倍率
# kirico_sagai_fight_record_length #战斗记录最大长度
# kirico_sagai_fight_elements_restrain #元素克制伤害倍率



def kirico_segai_config(config_name,default):
    try:
        if hasattr(main_config, config_name):
            return main_config.__getattribute__(config_name)
        else:
            return default
    except:
        return default