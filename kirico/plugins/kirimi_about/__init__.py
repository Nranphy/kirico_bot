from nonebot import get_driver, on_command, on_regex
from nonebot.adapters.onebot.v11 import Event, Bot, Message ,MessageSegment
from nonebot.params import State, CommandArg
from nonebot.typing import T_State
from nonebot.rule import to_me
from nonebot.log import logger


__kirico_plugin_name__ = '关于雾子酱☆'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.0.6'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '要查看雾子的信息吗~'

__kirico_plugin_usage__ = '''
at雾子并输入“关于”查看雾子关于信息√
对雾子的反馈和建议请使用【/反馈 xxx】，雾子会好好转达给作者桑的哦~
(ps.其中xxx为消息和图片，请在同一消息中发送。如有多段文本，可多次使用该指令哦~)
'''

__kirico__plugin_visible__ = True




about_request = on_regex("^关于$", priority=5, block=True, rule=to_me())

feedback_request = on_command("反馈", aliases={"建议","意见"}, priority=5, block=True)


@about_request.handle()
async def _():
    msg = f"""
米娜~这里是雾子酱哦√
插件功能帮助请输入【/help】
对雾子的反馈和建议请使用【/反馈 xxx】
联系作者：3102002900
开源仓库：https://github.com/nranphy/kirico_bot/
    """.strip()
    await about_request.send(msg)


@feedback_request.handle()
async def feedback(bot:Bot, event:Event, arg:Message = CommandArg()):
    try:
        qq_list = get_driver().config.superusers
    except:
        qq_list = list()
    if not qq_list:
        await feedback_request.finish("抱歉...未找到作者留下的联系方式×\n雾子酱...迷路了啦×")
    else:
        try:
            for qq in qq_list:
                await bot.send_private_msg(message="雾子收到新反馈哦~\n原消息如下、迷迭迷迭~\n=========\n"+arg+f"\n=========\n发送者【{event.get_user_id()}】\n来自群聊【{event.group_id}】", user_id=qq)
        except:
            await feedback_request.finish("抱歉...未找到管理员其一的联系方式×消息未全部送达...\n雾子酱...又迷路了啦×")
        await feedback_request.finish("成功传达哦~")