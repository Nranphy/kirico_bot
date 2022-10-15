from unittest import result
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Message, Event

import httpx



nbnhhsh_request = on_command("缩写", priority=10, block=True)


@nbnhhsh_request.handle()
async def nbnhhsh_process(event:Event, arg:Message=CommandArg()):
    word = arg.extract_plain_text().strip()

    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    result = httpx.post(
        url, 
        data={
            "text": word
            },
        timeout=10000).json()
    if not result:
        await nbnhhsh_request.finish("该字符不能查询哦~", at_sender=True)
    await nbnhhsh_request.finish((
        f"【{word}】可能的解释为：\n"+
        ('，'.join(result[0].get("trans",[])))
    ), at_sender=True)