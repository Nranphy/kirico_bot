import aiohttp
from nonebot.log import logger
from nonebot.params import T_State,State
from nonebot.plugin import on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, Message



__kirico_plugin_name__ = '能不能好好说话！！！'

__kirico_plugin_author__ = 'anlen123'

__kirico_plugin_version__ = '0.0.5'

__kirico_plugin_repositorie__ = 'https://github.com/anlen123/nonebot_plugin_abbrreply'

__kirico_plugin_description__ = 'u1s1用缩写真是duck不必（指指点点）'

__kirico_plugin_usage__ = '''
发送【缩写 xxx】来查找该字母缩写的可能解释~
果然还是好好说话比较好×
'''



__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True




async def get_sx(word):
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"

    headers = {
        'origin': 'https://lab.magiconch.com',
        'referer': 'https://lab.magiconch.com/nbnhhsh/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    }
    data = {
        "text": f"{word}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as resp:
            msg = await resp.json()
            return msg if msg else []


sx = on_regex(pattern="^sx\ |^缩写\ (.*)")




@sx.handle()
async def _(bot: Bot,event: Event, state:T_State=State()):
    msg = str(event.get_message())[3:]
    data = await get_sx(msg)
    result = ""
    try:
        data = data[0]
        name = data['name']
        try:
            content = data['trans']
            result += ' , '.join(content)
        except KeyError:
            pass
        try:
            inputs = data['inputting']
            result += ' , '.join(inputs)
        except KeyError:
            pass
        if result:
            logger.info(f"【 {name} 】可能解释为：\n{result}")
            await sx.finish(message=f"【 {name} 】可能解释为：\n{result}")
        await sx.finish(message=f"没有找到缩写 {msg} 的可能释义...")
    except KeyError:
        await sx.finish(message=f"出错啦")
    except IndexError:
        await sx.finish(message=f"该字符不能查询哦~")
