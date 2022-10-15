from nonebot import on_command
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER
import random

from kirico.utils.basic_utils import kirico_logger



dismiss = on_command("dismiss",aliases={"退群","退出群聊"},priority=1,block=True,permission=SUPERUSER|GROUP_OWNER|GROUP_ADMIN)


@dismiss.handle()
async def dismiss_comfirm(bot:Bot, event:GroupMessageEvent, state:T_State):
    string = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    state["random_str"] = ''.join([random.choice(string) for x in range(5)])
    await dismiss.send(f"真的要雾子退群吗...？\n请输入【{state['random_str']}】确认哦...",at_sender=True)

@dismiss.got("print")
async def dismiss_process(bot:Bot, event:GroupMessageEvent, state:T_State):
    if state["random_str"] == str(state["print"]):
        await dismiss.send(f"那么，雾子走了哦...\n大家以后也要开开心心的群聊...！！",at_sender=True)
        try:
            await bot.set_group_leave(group_id=event.group_id, is_dismiss=False)
        except:
            await dismiss.finish(f"雾子现在还是群主哦...请联系管理者移交群主吧×",at_sender=True)
        kirico_logger("info", "退群控制", f"雾子退出了群聊 {event.group_id}.")
    else:
        await dismiss.finish(f"验证码错误×\n需要雾子退群的话请再次输入【/退群】指令吧...",at_sender=True)