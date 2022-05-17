from nonebot import on_command, require, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.message import run_preprocessor
from nonebot.params import State, CommandArg, Arg, MatcherParam, EventParam
from nonebot.plugin.plugin import get_loaded_plugins, get_plugin
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, PrivateMessageEvent
from nonebot.exception import IgnoredException
from nonebot.log import logger
from kirico.utils.config_utils import get_config
from .utils import if_groupchat_on, if_plugin_on


driver = get_driver()

config = driver.config

# 指令开关插件
from .switch import *


# 各种钩子函数

@run_preprocessor
async def run_preprocessor_process(event: EventParam, matcher: MatcherParam):
    plugin_name = matcher.plugin_name
    group_id = event.group_id
    if isinstance(event,PrivateMessageEvent) or plugin_name=="kirimi_hooks":
        pass # 禁用对本管理插件与私聊信息不生效
    else:
        # 判断是否在该群禁用机器人
        if not if_groupchat_on(group_id):
            logger.info(f"[钩子函数] 本群（{group_id}）已禁用雾子...已忽略消息。")
            raise IgnoredException
        # 判断是否在该群禁用了插件
        if not if_plugin_on(group_id,plugin_name):
            logger.info(f"[钩子函数] 本群（{group_id}）已禁用该插件...插件名【{plugin_name}】。")
            raise IgnoredException