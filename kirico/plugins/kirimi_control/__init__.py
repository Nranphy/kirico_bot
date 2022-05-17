from nonebot import on_command, require, get_bot, get_driver
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.message import run_preprocessor
from nonebot.params import State, CommandArg, Arg, MatcherParam, EventParam
from nonebot.plugin.plugin import get_loaded_plugins, get_plugin
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, PrivateMessageEvent
from nonebot.exception import IgnoredException
from nonebot.log import logger
from kirico.utils.config_utils import get_config
from .utils import if_groupchat_on, if_plugin_on


__kirico_plugin_name__ = '雾子酱控制器'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.0.5'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '雾子...读取完毕——'

__kirico_plugin_usage__ = '''
控制雾子酱在群聊时的表现√
===
需要在不同群开关插件吗？用【/help】获得插件英文名再使用以下命令控制√
【/关闭插件 xxx】xxx为获取的插件英文名
【/开启插件 xxx】xxx为获取的插件英文名
插件默认均为开启哦~ 另外本管理插件不能禁用√
===
本群有风险或者暂时不需要雾子，可以暂时关闭雾子哦
【/关闭】关闭雾子所有其他功能，只留下本插件
【/开启】恢复雾子所有功能，但不会重置插件开关哦
===
不需要雾子了吗...？请使用安全的退群方式哦...
【/退群】可按提示让雾子安全的退群
'''

__kirico__plugin_visible__ = True






driver = get_driver()

config = driver.config


# 指令开关插件
from .switch import *

# 退群指令
from .dismiss import *


# 各种钩子函数

@run_preprocessor
async def run_preprocessor_process(event:Event = EventParam(), matcher:Matcher = MatcherParam):
    plugin_name = matcher.plugin_name
    group_id = event.group_id
    if isinstance(event,PrivateMessageEvent) or plugin_name==__package__.split('.')[-1]:
        pass # 禁用对本管理插件与私聊信息不生效
    else:
        # 判断是否在该群禁用机器人
        if not if_groupchat_on(group_id):
            logger.info(f"[钩子函数] 本群（{group_id}）已禁用雾子...已忽略消息。")
            raise IgnoredException("雾子在该群已禁用...")
        # 判断是否在该群禁用了插件
        if not if_plugin_on(group_id,plugin_name):
            logger.info(f"[钩子函数] 本群（{group_id}）已禁用该插件...插件名【{plugin_name}】。")
            raise IgnoredException("插件在该群已禁用...")