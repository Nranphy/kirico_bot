'''消息处理类工具'''

from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, GroupMessageEvent, MessageEvent

from nonebot_plugin_htmlrender import get_new_page, md_to_pic
from typing import List, Union
import json
import re

from kirico.utils.pic_utils import get_img, save_img, get_pic_md5






async def edit_img_message(msg:Message,path = "data/pic_temp/") -> Message:
    '''
    对传入Message进行处理，下载图片并替换图片data地址。
    :param msg: 传入的消息段
    :param path: 存储图片的目录，请注意“/”结尾。默认为bot根目录data/pic_temp/
    :返回新Message，失败则返回False.
    '''
    new_msg = Message()
    for seg in msg:
        if seg.type == "image":
            url = seg.data.get("url", "")
            filename = seg.data.get("file", "")
            if filename and url:
                img = await get_img(url)
                if img:
                    path = path + f"{filename}"
                    await save_img(img, path)
                    seg.data["file"] = f"file:///"+path
                else:
                    return False
        new_msg.append(seg)
    return new_msg


def is_text(msg:Message) -> bool:
    '''判断传入消息是否为纯文本消息（空Message也视为文本消息）'''
    for ms in msg:
        if ms.type != 'text':
            return False
    return True


def get_message_at(msg:Message) -> list:
    '''
    获取传入消息内at的qq号或者数字qq号list，如不存在则返回空列表
    '''
    ans = list()
    for m in msg["at"]:
        ans.append(m.data.get("qq",""))
    for i in msg["text"]:
        text = i.data.get("text","")
        if text.isnumeric():
            ans.append(text)
    return ans

async def send_forward_msg(
    bot: Bot,
    event: MessageEvent,
    name: str,
    uin: str,
    msgs: List[str],
):
    '''
    感谢wq佬和他的remake插件！！
    发送群合并消息
    '''
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    if getattr(event,"group_id",None):
        messages = [to_json(msg) for msg in msgs]
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        md_str = f'# {name}\n***\n'+'\n***\n'.join(msgs)
        pic = await md_to_pic(md_str)
        await bot.send(event,MessageSegment.image(pic),at_sender=True)

def message_equal(a:Message, b:Message) -> bool:
    '''判断两个Message是否相同，只考虑了text, face, image, at四种消息段'''
    n = len(a)
    if n != len(b):
        return False
    for i in range(n):
        if a[i].type != b[i].type:
            return False
        if a[i].type == 'text' and a[i] == b[i]:
            continue
        elif a[i].type == 'face' and a[i].data.get("id") == b[i].data.get("id"):
            continue
        elif a[i].type == 'image' and get_pic_md5(a[i]) == get_pic_md5(b[i]):
            continue
        elif a[i].type == 'at' and a[i].data.get("qq") == b[i].data.get("qq"):
            continue
        else:
            return False
    return True