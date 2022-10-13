from nonebot import get_bot, on_notice, on_command
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, Message, PokeNotifyEvent
from nonebot.log import logger
from kirico.utils.friendliness_utils import friendliness_change
from kirico.utils.basic_utils import get_date_and_time
from random import choice,random
import json



__kirico_plugin_name__ = '雾子酱戳戳~'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.0.5'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '戳你戳我戳他戳她戳...不准戳啦！！'

__kirico_plugin_usage__ = '''
向雾子戳一戳的话，会被戳回来吧...
或许会增长好感度哦——会下降也说不定×
向雾子酱发送指令【/戳 xxx】也可以让雾子戳别人哦~
（ps.指令中的xxx可以是at或者QQ号）
'''



__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True






poke_command = on_command("poke", aliases={"戳","戳一戳","戳他"}, priority=10, block=True)

@poke_command.handle()
async def __pokewho__(event: Event, state: T_State = State()):
    message = str(event.get_message()).split()
    try:
        state["item"] = message[1]
    except Exception:
        pass

@poke_command.got("item", prompt="要雾子戳谁呢~\nat他吧~")
async def pokeother(bot: Bot, event: Event, state: T_State = State()):
    state["item"] = str(state["item"])
    if state["item"].isnumeric():
        pass
    else:
        try:
            state["item"] = state["item"][10:-1]
        except Exception:
            pass
    logger.info("戳他戳他！")
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
    logger.info("雾子收到了戳一戳！！")
    sender_qq = event.get_user_id()
    random_flag = random()
    friendliness_change(event.get_user_id(),5,10,note="戳了戳雾子...")
    if random_flag < 0.3:
        logger.info("回复ta吧×")
        await PokeNotify_notice.finish(choice([
            "不准戳不准戳！！！", 
            "不要戳啦！！呜呜呜", 
            "再戳雾子就生气了！", 
            "真的有那么好戳吗..."]))
    else:
        logger.info("戳回去戳回去！")
        await bot.send(event, Message(f"[CQ:poke,qq={sender_qq}]"))