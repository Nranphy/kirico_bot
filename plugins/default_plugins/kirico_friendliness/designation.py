from nonebot import on_command
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, Message, GroupMessageEvent

from utils.friendliness_utils import KiricoFriendliness






nickname_setting_request = on_command("nickname", aliases={"设置别名","叫我","设置称呼","设置昵称","设定称呼","设定昵称","设定别名"}, priority=7, block=True)

special_title_setting_request = on_command("设置头衔", aliases={"头衔设置","头衔","专属头衔"}, priority=7, block=True)



@nickname_setting_request.handle()
async def nickname_setting_prepare(bot:Bot, event:Event, state:T_State, arg:Message=CommandArg()):
    arg = arg.extract_plain_text().strip()
    if arg:
        state["nickname"] = arg


@nickname_setting_request.got("nickname",prompt="想要雾子怎样称呼你呢~")
async def nickname_setting(bot:Bot, event:Event, state:T_State):
    qq = event.get_user_id()
    if isinstance(state["nickname"], Message):
        new_nickname = state["nickname"].extract_plain_text()
    else:
        new_nickname = state["nickname"]
    friendliness_info = KiricoFriendliness(qq)

    if friendliness_info.count < 200:
        await nickname_setting_request.finish("雾子和你还不是很熟哦...和雾子先从朋友做起好吗？", at_sender=True)

    friendliness_info.set_nickname(new_nickname)
    await nickname_setting_request.finish(f"雾子记住了哦~ {new_nickname}√", at_sender=True)



@special_title_setting_request.handle()
async def special_title_setting_prepare(bot:Bot, event:GroupMessageEvent, state:T_State, arg:Message=CommandArg()):
    special_title = arg.extract_plain_text().strip()

    qq = event.get_user_id()
    friendliness_info = KiricoFriendliness(qq)

    if friendliness_info.count < 50:
        await special_title_setting_request.finish("雾子...还和你不是很熟呢×", at_sender=True)

    try:
        await bot.set_group_special_title(group_id=event.group_id, user_id=qq, special_title=special_title)
        await special_title_setting_request.finish("设置成功哦~", at_sender=True)
    except:
        await special_title_setting_request.finish("设置失败呢...\n请检查头衔是否在六个字以内并没有特殊字符哦~", at_sender=True)