from typing import Union
from nonebot import on_command, on_regex, require, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.plugin.plugin import get_loaded_plugins, get_plugin
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.exception import IgnoredException
from nonebot.log import logger
import random



dismiss = on_command("dismiss",aliases={"退群","退出群聊"},priority=1,block=True,permission=SUPERUSER|GROUP_OWNER|GROUP_ADMIN)


@dismiss.handle()
async def dismiss_comfirm(bot:Bot, event:GroupMessageEvent, state:T_State = State()):
    string = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    state["random_str"] = ''.join([random.choice(string) for x in range(5)])
    await dismiss.send(f"真的要雾子退群吗...？\n请输入【{state['random_str']}】确认哦...",at_sender=True)

@dismiss.got("print")
async def dismiss_process(bot:Bot, event:GroupMessageEvent, state:T_State = State()):
    if state["random_str"] == str(state["print"]):
        await dismiss.send(f"那么，雾子走了哦...\n大家以后也要开开心心的群聊...！！",at_sender=True)
        try:
            await bot.set_group_leave(group_id=event.group_id)
        except:
            await dismiss.finish(f"雾子现在还是群主哦...请联系管理者移交群主吧×\n雾子也不想大家分散呢...",at_sender=True)
    else:
        await dismiss.finish(f"验证码错误×\n需要雾子退群的话请再输入【/退群】指令吧...",at_sender=True)