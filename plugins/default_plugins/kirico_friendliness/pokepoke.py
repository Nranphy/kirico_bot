from nonebot import get_bot, on_notice, on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, Message, PokeNotifyEvent

from random import choice,random

from utils.friendliness_utils import KiricoFriendliness


poke_command = on_command("poke", aliases={"戳","戳一戳","戳他"}, priority=10, block=True)

@poke_command.handle()
async def __pokewho__(event: Event, state: T_State):
    message = str(event.get_message()).split()
    try:
        state["item"] = message[1]
    except Exception:
        pass

@poke_command.got("item", prompt="要雾子戳谁呢~\nat他吧~")
async def pokeother(bot: Bot, event: Event, state: T_State):
    state["item"] = str(state["item"])
    if state["item"].isnumeric():
        pass
    else:
        try:
            state["item"] = state["item"][10:-1]
        except Exception:
            pass
    if state["item"] == get_bot().self_id or state["item"] == '':
        await poke_command.finish("笨蛋~！！\n雾子才不会戳自己呢//v//")
    else:
        await bot.send(event, Message("[CQ:poke,qq={}]".format(state["item"])))






async def __PokeNotify__(bot: Bot, event: Event) -> bool:
    if isinstance(event,PokeNotifyEvent) and event.is_tome():
        return True
    return False

PokeNotify_notice = on_notice(__PokeNotify__, priority=10)

@PokeNotify_notice.handle()
async def reply_poke(bot: Bot, event: Event):
    sender_qq = event.get_user_id()
    friendliness_info = KiricoFriendliness(sender_qq)
    friendliness_info.change(5, 10, note="戳了戳雾子...")

    if random() < 0.3:
        await PokeNotify_notice.finish(choice([
            "不准戳不准戳！！！", 
            "不要戳啦！！呜呜呜", 
            "再戳雾子就生气了！", 
            "真的有那么好戳吗..."]))
    else:
        await bot.send(event, Message(f"[CQ:poke,qq={sender_qq}]"))