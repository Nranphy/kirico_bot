from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, GroupMessageEvent, MessageEvent
from kirico.utils.pic_utils import get_img, save_img
from typing import List, Union
import json






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

    if isinstance(event,GroupMessageEvent):
        messages = [to_json(msg) for msg in msgs]
        await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        await bot.send(event,"私聊与频道暂时无法发送合并消息哦~敬请期待√",at_sender=True)