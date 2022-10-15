import random
from re import I

import nonebot
from nonebot import on_command, on_regex, get_driver
from nonebot.adapters.onebot.v11 import (Bot, Event, Message,
                                         PrivateMessageEvent,
                                         GroupMessageEvent)
from nonebot.adapters.onebot.v11.permission import GROUP, PRIVATE_FRIEND
from nonebot.log import logger
from nonebot.typing import T_State
from .get_data import get_setu
from .setu_message import *
from .json_manager import *
from .config import Config

global_config = get_driver().config
config: Config = Config.parse_obj(global_config.dict())

setu = on_regex(
    r"^(setu|来点色图|涩图|来点涩图|色图|涩屠|来点涩屠)\s?(r18)?\s?(.*)?",
    flags=I,
    permission=PRIVATE_FRIEND | GROUP,
)

cdTime = (config.setu2_cd if config.setu2_cd else 60)

#if not config.proxies_socks5:
#    logger.warning("未检测到代理, 请检查是否正常访问 i.pixiv.cat.")


@setu.handle()
async def _(bot: Bot, event: Event, state: T_State):
#    if isinstance(event, GroupMessageEvent) and event.group_id not in config.setu2_enable_groups:
#        return
    global mid
    args = list(state["_matched_groups"])
    r18 = args[1]
    key = args[2]
    qid = event.get_user_id()
    mid = event.message_id
    data = readJson()
    try:
        cd = event.time - data[qid][0]
    except Exception:
        cd = cdTime + 1

    r18 = True if (isinstance(event, PrivateMessageEvent) and r18) else False

    logger.info(f"key={key},r18={r18}")

    if (cd > cdTime or event.get_user_id() in config.superusers
            or isinstance(event, PrivateMessageEvent)):
        writeJson(qid, event.time, mid, data)
        pic = await get_setu(key, r18)
        if pic[2]:
            try:
                await setu.send(
                    at_sender=True,
                    message=Message(pic[1])+Message(pic[0])
                )
                #await setu.send(message=Message(pic[0]))
            except Exception as e:
                logger.warning(e)
                removeJson(qid)
                await setu.finish(
                    message=Message(f"图片消息被风控了呜呜呜\n{pic[1]}\n只保留了链接哦...\n{pic[3]}"),
                    at_sender=True,
                )

        else:
            removeJson(qid)
            await setu.finish(pic[0] + pic[1])

    else:
        time_last = cdTime - cd
        hours, minutes, seconds = 0, 0, 0
        if time_last >= 60:
            minutes, seconds = divmod(time_last, 60)
            hours, minutes = divmod(minutes, 60)
        else:
            seconds = time_last
        cd_msg = f"{str(hours) + '小时' if hours else ''}{str(minutes) + '分钟' if minutes else ''}{str(seconds) + '秒' if seconds else ''}"

        await setu.send(f"{random.choice(setu_send_cd)} 你的CD还有{cd_msg}",
                        at_sender=True)
