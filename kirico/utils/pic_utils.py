from nonebot.log import logger
import aiofiles
import httpx







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


async def save_img(img: bytes, path: str):
    '''
    保存变量中的图片
    :param img: 需要保存的图片
    :param path: 保存图片的绝对地址
    '''
    async with aiofiles.open(str(path), "wb") as f:
        await f.write(img)