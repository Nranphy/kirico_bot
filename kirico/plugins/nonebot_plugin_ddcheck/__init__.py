import traceback
from loguru import logger
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.log import logger

from .data_source import get_reply



__kirico_plugin_name__ = '成分姬~'

__kirico_plugin_author__ = 'MeetWq'

__kirico_plugin_version__ = '0.1.0'

__kirico_plugin_repositorie__ = 'https://github.com/MeetWq/nonebot-plugin-ddcheck'

__kirico_plugin_description__ = '让雾子康康！！'

__kirico_plugin_usage__ = '''
输入【/查成分 xxx】可查询该用户在B站的关注和粉丝牌哦~
（ps.指令中xxx为B站用户名或者UID）
展示的是VTB、舟、原等相关up~
'''

__kirico__plugin_visible__ = True



__help__plugin_name__ = "ddcheck"
__des__ = "成分姬"
__cmd__ = """
查成分 {用户名/UID}
""".strip()
__short_cmd__ = __cmd__
__example__ = """
查成分 小南莓Official
""".strip()
__usage__ = f"{__des__}\nUsage:\n{__cmd__}\nExample:\n{__example__}"


ddcheck = on_command("查成分", block=True, priority=12)


@ddcheck.handle()
async def _(msg: Message = CommandArg()):
    text = msg.extract_plain_text().strip()
    if not text:
        await ddcheck.finish()

    try:
        res = await get_reply(text)
    except:
        logger.warning(traceback.format_exc())
        await ddcheck.finish("出错了，请稍后再试")

    if isinstance(res, str):
        await ddcheck.finish(res)
    else:
        await ddcheck.finish(MessageSegment.image(res))
