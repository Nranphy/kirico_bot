from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.params import MatcherParam, EventParam
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, PrivateMessageEvent
from nonebot.exception import IgnoredException

from typing import Dict, Any

from kirico.utils.basic_utils import kirico_logger

from .utils import if_groupchat_on, if_plugin_on



@run_preprocessor
async def run_preprocessor_process(event:Event = EventParam(), matcher:Matcher = MatcherParam()):
    plugin_name = matcher.plugin_name
    if isinstance(event, PrivateMessageEvent) or plugin_name==__package__.split('.')[-1]:
        pass # 禁用对本管理插件与私聊信息不生效
    elif isinstance(event, GroupMessageEvent):
        group_id = getattr(event, "group_id")
        # 判断是否在该群禁用机器人
        if not if_groupchat_on(group_id):
            kirico_logger("info", "雾子控制", f"本群（{group_id}）已禁用雾子...已忽略消息。")
            raise IgnoredException("雾子在该群已禁用...")
        # 判断是否在该群禁用了插件
        if not if_plugin_on(group_id, plugin_name):
            kirico_logger("info", "雾子控制", f"本群（{group_id}）已禁用该插件...插件名【{plugin_name}】。")
            raise IgnoredException("插件在该群已禁用...")

@Bot.on_calling_api
async def on_calling_api_process(api: str, data: Dict[str, Any]):
    # 只对发送群消息API起约束作用
    if not api == "send_group_msg":
        return
    group_id = data.get("group_id")
    if group_id and not if_groupchat_on(group_id):
        kirico_logger("info", "雾子控制", f"本群（{group_id}）已禁用雾子...已忽略消息。")
        raise IgnoredException("雾子在该群已禁用...")