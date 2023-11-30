import re

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.log import logger

from .analysis_bilibili import b23_extract, bili_keyword



__kirico_plugin_name__ = '雾子的bilibili解析'

__kirico_plugin_author__ = 'NekoAria'

__kirico_plugin_version__ = '0.0.5'

__kirico_plugin_repositorie__ = 'https://github.com/NekoAria/nonebot_plugin_analysis_bilibili'

__kirico_plugin_description__ = 'B站...是什么呢...？'

__kirico_plugin_usage__ = '''
群内或私信发送B站链接或分享后，雾子会自动返回链接解析~
'''

__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True







analysis_bili = on_regex(
    r"(b23.tv)|(bili(22|23|33|2233).cn)|(.bilibili.com)|(^(av|cv)(\d+))|(^BV([a-zA-Z0-9]{10})+)|"
    r"(\[\[QQ小程序\]哔哩哔哩\])|(QQ小程序&amp;#93;哔哩哔哩)|(QQ小程序&#93;哔哩哔哩)",
    flags=re.I,
)


@analysis_bili.handle()
async def analysis_main(event: MessageEvent) -> None:
    text = str(event.message).strip()
    if re.search(r"(b23.tv)|(bili(22|23|33|2233).cn)", text, re.I):
        # 提前处理短链接，避免解析到其他的
        text = await b23_extract(text)
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    msg = await bili_keyword(group_id, text)
    if msg:
        try:
            await analysis_bili.send("锵锵~雾子已解析B站链接√\n=========\n"+msg)
        except Exception as e:
            logger.error(e)
