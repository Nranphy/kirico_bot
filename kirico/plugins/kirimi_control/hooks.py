from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.params import MatcherParam, EventParam
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, PrivateMessageEvent
from nonebot.exception import IgnoredException
from nonebot.log import logger
from .utils import if_groupchat_on, if_plugin_on



@run_preprocessor
async def run_preprocessor_process(event:Event = EventParam(), matcher:Matcher = MatcherParam):
    plugin_name = matcher.plugin_name
    group_id = getattr(event,"group_id",None)
    if isinstance(event,PrivateMessageEvent) or plugin_name==__package__.split('.')[-1]:
        pass # 禁用对本管理插件与私聊信息不生效
    elif isinstance(event,GroupMessageEvent):
        # 判断是否在该群禁用机器人
        if not if_groupchat_on(group_id):
            logger.info(f"[钩子函数] 本群（{group_id}）已禁用雾子...已忽略消息。")
            raise IgnoredException("雾子在该群已禁用...")
        # 判断是否在该群禁用了插件
        if not if_plugin_on(group_id,plugin_name):
            logger.info(f"[钩子函数] 本群（{group_id}）已禁用该插件...插件名【{plugin_name}】。")
            raise IgnoredException("插件在该群已禁用...")