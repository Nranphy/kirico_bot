from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event, Bot, Message
from nonebot.params import CommandArg

from kirico.utils.basic_utils import kirico_logger, get_config



feedback_request = on_command("反馈", aliases={"建议","意见","提交建议","提交意见"}, priority=5, block=True)



@feedback_request.handle()
async def feedback(bot:Bot, event:Event, arg:Message = CommandArg()):
    super_users = get_config("superusers", [], list)
    if not super_users:
        await feedback_request.finish("抱歉...未找到作者留下的联系方式×\n雾子酱...迷路了啦×")
    for qq in super_users:
        try:
            await bot.send_private_msg(message=(
                "雾子收到新反馈哦~\n"
                "原消息如下、迷迭迷迭~\n"
                "=========\n"
                f"{arg}\n"
                f"=========\n"
                f"发送者【{event.get_user_id()}】\n"
                f"来自群聊【{event.group_id}】"), user_id=qq)
        except:
            kirico_logger("error", "意见反馈", f"向 {qq} 发送反馈失败，请检查.env设置和bot好友或机器人风控。")
    await feedback_request.finish("成功传达哦~")