'''图片相关操作工具'''

from hashlib import md5
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import MessageSegment

import aiofiles
import httpx
from pathlib import Path
from typing import Union

from kirico.utils.basic_utils import get_config
from kirico.utils.file_utils import check_dir



temp_img_path = get_config("temp_img_path", Path("data/temp/img/"), Path)




async def get_img(url:str) -> bytes:
    '''
    获取链接中的图片。
    :param url: 图片直链
    :如果网站非图片直链，返回值不可测。获取图片失败时返回False.
    '''
    try:
        async with httpx.AsyncClient() as client:
            pic = await client.get(url)
            return pic.content
    except Exception as e:
        logger.warning(f"[图片工具]获取图片时出错,错误原因{e}。{url}")
        return False


async def save_img(img: bytes, path: Union[str,Path] = temp_img_path):
    '''
    保存变量中的图片
    :param img: 需要保存的图片
    :param path: 保存图片的绝对地址
    '''
    async with aiofiles.open(path, "wb") as f:
        await f.write(img)


def get_pic_md5(ms:MessageSegment) -> str:
    '''获取图片消息段的MD5编码，出错则返回空字符串'''
    try:
        pic = httpx.get(ms.data.get("url")).content
    except:
        return ''
    return md5(pic).hexdigest()