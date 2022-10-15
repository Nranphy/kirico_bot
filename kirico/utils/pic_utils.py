'''图片相关操作工具'''


from nonebot.adapters.onebot.v11 import MessageSegment

import httpx
from asyncio import run
from hashlib import md5
from pathlib import Path
from typing import Optional, Union

from .basic_utils import kirico_logger
from .file_utils import check_dir, kirico_cache_path



kirico_img_temp_path = kirico_cache_path / "img/"
'''图片文件临时目录'''

check_dir(kirico_img_temp_path)




async def get_img(url: str) -> Optional[bytes]:
    '''
    从图片直链中获取图片。
    :param url: 图片直链
    :rtype: 如果网站非图片直链，则返回值不可测。获取图片失败时返回None.
    '''
    try:
        async with httpx.AsyncClient() as client:
            pic = await client.get(url)
            return pic.content
    except Exception as e:
        kirico_logger("error", "图片工具", f"获取图片时出错，错误原因 【{e}】，图片链接为 【{url}】。")
        return None


def save_img(img: bytes, path: Union[str,Path] = kirico_img_temp_path):
    '''
    保存bytes变量中的图片。
    :param img: 需要保存的图片
    :param path: 保存图片的路径
    '''
    with open(path, "wb") as f:
        f.write(img)


def get_pic_md5(ms:MessageSegment) -> str:
    '''获取图片消息段的MD5编码，出错则返回空字符串'''
    try:
        pic = run(get_img(ms.data.get("url")))
    except:
        return ''
    return md5(pic).hexdigest()