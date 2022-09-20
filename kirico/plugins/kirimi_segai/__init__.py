from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
from kirico.utils.file_utils import check_dir, check_file
import time
import os
import json

__kirico_plugin_name__ = '雾境'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.1.0'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '群聊中的养成RPG小游戏'

__kirico_plugin_usage__ = '''
雾境相关指令和帮助请用【/雾境】查看哦
'''



__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True



# 账号相关

from .account import *



# 游戏系统
## 日常
from .daily import *
## 战斗
from .fighting import *



# 雾境查询

from .dictionary import *