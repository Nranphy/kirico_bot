from nonebot import on_regex, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, MessageSegment, Message



report_req = on_regex("^举报$", priority=3, block=True)


async def get_owmer(bot:Bot, group_id:int):
    member_ls = await bot.call_api("get_group_member_list", group_id = int(group_id))
    for mem in member_ls:
        if mem["role"] == "owner":
            return mem["user_id"]

@report_req.handle()
async def report_handler(bot:Bot, event:GroupMessageEvent, state:T_State):
    group_owner = await get_owmer(bot, event.group_id)
    state["group_owner"] = group_owner
    await report_req.send(
        "欢迎使用直通群主举报热线:\n"
        "涩图请按1\n"
        "涉赌请按2\n"
        "键政请按3\n"
        "小广告请按4\n"
        "调戏妹子请按5\n"
        "南通梗请按6\n"
        "肯德基梗请按7\n"
        "造谣传谣请按8\n"
        "刷屏扰民请按9\n"
        "黑群主请按0\n"
        "情侣秀恩爱请按#\n"
        "=============\n"
        "请输入要举报的类型~", at_sender=True
    )

@report_req.got("option")
async def report_got_handler(state:T_State):
    msg:Message = state["option"]
    text = msg.extract_plain_text()
    if not text or text[0] not in list("1234567890#"):
        await report_req.finish()
    await report_req.send(MessageSegment.at(state["group_owner"]))