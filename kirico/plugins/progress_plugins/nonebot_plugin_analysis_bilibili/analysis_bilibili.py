import json
import re
import time
import urllib.parse

import aiohttp
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.log import logger

analysis_stat = {}  # analysis_stat: video_url(vurl)


async def bili_keyword(group_id, text):
    try:
        # 提取url
        url, page = extract(text)
        # 如果是小程序就去搜索标题
        if not url:
            pattern = re.compile(r'"desc":"[^"]*"')
            desc = re.findall(pattern, text)
            i = 0
            while i < len(desc):
                title_dict = "{" + desc[i] + "}"
                title = json.loads(title_dict)
                i += 1
                if title["desc"] == "哔哩哔哩":
                    continue
                vurl = await search_bili_by_title(title["desc"])
                if vurl:
                    url, page = extract(vurl)
                    break

        # 获取视频详细信息
        msg, vurl = "", ""
        if "view?" in url:
            msg, vurl = await video_detail(url, page)
        elif "bangumi" in url:
            msg, vurl = await bangumi_detail(url)
        elif "xlive" in url:
            msg, vurl = await live_detail(url)
        elif "article" in url:
            msg, vurl = await article_detail(url, page)
        elif "dynamic" in url:
            msg, vurl = await dynamic_detail(url)

        # 避免多个机器人解析重复推送
        last_vurl = ""
        if group_id:
            if group_id in analysis_stat:
                last_vurl = analysis_stat[group_id]
            analysis_stat[group_id] = vurl
        if last_vurl == vurl:
            return
    except Exception as e:
        logger.error(e)
        msg = ""
    return msg


async def b23_extract(text):
    b23 = re.compile(r"b23.tv/(\w+)|(bili(22|23|33|2233).cn)/(\w+)", re.I).search(
        text.replace("\\", "")
    )
    url = f"https://{b23[0]}"
    async with aiohttp.request("GET", url) as resp:
        return str(resp.url)


def extract(text: str):
    try:
        page = re.compile(r"([?&]|&amp;)p=\d+").search(text)
        aid = re.compile(r"av\d+", re.I).search(text)
        bvid = re.compile(r"BV([A-Za-z0-9]{10})+", re.I).search(text)
        epid = re.compile(r"ep\d+", re.I).search(text)
        ssid = re.compile(r"ss\d+", re.I).search(text)
        mdid = re.compile(r"md\d+", re.I).search(text)
        room_id = re.compile(r"live.bilibili.com/(blanc/|h5/)?(\d+)", re.I).search(text)
        cvid = re.compile(
            r"(/read/(cv|mobile|native)(/|\?id=)?|^cv)(\d+)", re.I
        ).search(text)
        dynamic_id_type2 = re.compile(
            r"([tm]).bilibili.com/(\d+)\?(.*?)(&|&amp;)type=2", re.I
        ).search(text)
        dynamic_id = re.compile(r"([tm]).bilibili.com/(\d+)", re.I).search(text)
        url = ""
        if bvid:
            url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid[0]}"
        elif aid:
            url = f"https://api.bilibili.com/x/web-interface/view?aid={aid[0][2:]}"
        elif epid:
            url = (
                f"https://bangumi.bilibili.com/view/web_api/season?ep_id={epid[0][2:]}"
            )
        elif ssid:
            url = f"https://bangumi.bilibili.com/view/web_api/season?season_id={ssid[0][2:]}"
        elif mdid:
            url = f"https://bangumi.bilibili.com/view/web_api/season?media_id={mdid[0][2:]}"
        elif room_id:
            url = f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id[2]}"
        elif cvid:
            page = cvid[4]
            url = f"https://api.bilibili.com/x/article/viewinfo?id={page}&mobi_app=pc&from=web"
        elif dynamic_id_type2:
            url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?rid={dynamic_id_type2[2]}&type=2"
        elif dynamic_id:
            url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={dynamic_id[2]}"
        return url, page
    except Exception as e:
        logger.error(e)
        return "", None


async def search_bili_by_title(title: str):
    search_url = f"https://api.bilibili.com/x/web-interface/search/all/v2?keyword={urllib.parse.quote(title)}"

    async with aiohttp.request("GET", search_url) as resp:
        result = (await resp.json())["data"]["result"]

        for i in result:
            if i.get("result_type") != "video":
                continue
            # 只返回第一个结果
            return i["data"][0].get("arcurl")


async def video_detail(url, page):
    try:
        async with aiohttp.request("GET", url) as resp:
            res = (await resp.json()).get("data")
            if not res:
                return "解析到视频被删了/稿件不可见或审核中/权限不足", url
            vurl = f"https://www.bilibili.com/video/av{res['aid']}"
            title = f"标题：{res['title']}\n"
            image = MessageSegment.image(res["pic"])
            if page:
                page = page[0].replace("&amp;", "&")
                p = int(page[3:])
                if p <= len(res["pages"]):
                    vurl += f"?p={p}"
                    part = res["pages"][p - 1]["part"]
                    if part != res["title"]:
                        title += f"小标题：{part}\n"
            tname = f"类型：{res['tname']} | UP：{res['owner']['name']}\n"
            stat = f"播放：{res['stat']['view']} | 弹幕：{res['stat']['danmaku']} | 收藏：{res['stat']['favorite']}\n"
            stat += f"点赞：{res['stat']['like']} | 硬币：{res['stat']['coin']} | 评论：{res['stat']['reply']}\n"
            desc = f"简介：{res['desc']}"
            desc_list = desc.split("\n")
            desc = "".join(i + "\n" for i in desc_list if i)
            desc_list = desc.split("\n")
            if len(desc_list) > 4:
                desc = desc_list[0] + "\n" + desc_list[1] + "\n" + desc_list[2] + "……"
            msg = Message()
            msg.extend([title, image, f"{vurl}\n", tname, stat, desc])
            return msg, vurl
    except Exception as e:
        logger.error(f"视频解析出错--Error:\n{e}")
        return "", ""


async def bangumi_detail(url):
    try:
        async with aiohttp.request("GET", url) as resp:
            res = (await resp.json()).get("result")
            if not res:
                return None, None
            cover = MessageSegment.image(res["cover"])
            title = f"番剧：{res['title']}\n"
            desc = f"{res['newest_ep']['desc']}\n"
            index_title = ""
            style = "".join(f"{i}," for i in res["style"])
            style = f"类型：{style[:-1]}\n"
            evaluate = f"简介：{res['evaluate']}\n"
            if "season_id" in url:
                vurl = f"https://www.bilibili.com/bangumi/play/ss{res['season_id']}\n"
            elif "media_id" in url:
                vurl = f"https://www.bilibili.com/bangumi/media/md{res['media_id']}\n"
            else:
                epid = re.compile(r"ep_id=\d+").search(url)[0][len("ep_id=") :]
                for i in res["episodes"]:
                    if str(i["ep_id"]) == epid:
                        index_title = f"标题：{i['index_title']}\n"
                        break
                vurl = f"https://www.bilibili.com/bangumi/play/ep{epid}\n"
            msg = Message()
            msg.extend([title, cover, f"{vurl}\n", index_title, desc, style, evaluate])
            return msg, vurl
    except Exception as e:
        logger.error(f"番剧解析出错--Error:\n{e}")
        return "", ""


async def live_detail(url):
    try:
        async with aiohttp.request("GET", url) as resp:
            res = await resp.json()
            if res["code"] != 0:
                return None, None
            res = res["data"]
            uname = res["anchor_info"]["base_info"]["uname"]
            room_id = res["room_info"]["room_id"]
            cover = MessageSegment.image(res["room_info"]["cover"])
            title = res["room_info"]["title"]
            live_status = res["room_info"]["live_status"]
            lock_status = res["room_info"]["lock_status"]
            parent_area_name = res["room_info"]["parent_area_name"]
            area_name = res["room_info"]["area_name"]
            online = res["room_info"]["online"]
            tags = res["room_info"]["tags"]
            watched_show = res["watched_show"]["text_large"]
            vurl = f"https://live.bilibili.com/{room_id}\n"
            if lock_status:
                lock_time = res["room_info"]["lock_time"]
                lock_time = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(lock_time)
                )
                title = f"[已封禁]直播间封禁至：{lock_time}\n"
            elif live_status == 1:
                title = f"[直播中]标题：{title}\n"
            elif live_status == 2:
                title = f"[轮播中]标题：{title}\n"
            else:
                title = f"[未开播]标题：{title}\n"
            up = f"主播：{uname} 当前分区：{parent_area_name}-{area_name}\n"
            watch = f"观看：{watched_show} 直播时的人气上一次刷新值：{online}\n"
            if tags:
                tags = f"标签：{tags}\n"
            if live_status:
                player = f"独立播放器：https://www.bilibili.com/blackboard/live/live-activity-player.html?enterTheRoom=0&cid={room_id}"
            else:
                player = ""
            msg = Message()
            msg.extend([title, cover, f"{vurl}\n", up, watch, tags, player])
            return msg, vurl
    except Exception as e:
        logger.error(f"直播间解析出错--Error:\n{e}")
        return "", ""


async def article_detail(url, cvid):
    try:
        async with aiohttp.request("GET", url) as resp:
            res = (await resp.json()).get("data")
            if not res:
                return None, None
            images = [MessageSegment.image(i) for i in res["origin_image_urls"]]
            vurl = f"https://www.bilibili.com/read/cv{cvid}\n"
            title = f"标题：{res['title']}\n"
            up = f"作者：{res['author_name']} (https://space.bilibili.com/{res['mid']})\n"
            view = f"阅读数：{res['stats']['view']} "
            favorite = f"收藏数：{res['stats']['favorite']} "
            coin = f"硬币数：{res['stats']['coin']}"
            share = f"分享数：{res['stats']['share']} "
            like = f"点赞数：{res['stats']['like']} "
            dislike = f"不喜欢数：{res['stats']['dislike']}"
            desc = view + favorite + coin + "\n" + share + like + dislike
            msg = Message(title)
            msg.extend(images)
            msg.extend([f"{vurl}\n", up, desc])
            return msg, vurl
    except Exception as e:
        logger.error(f"专栏解析出错--Error:\n{e}")
        return "", ""


async def dynamic_detail(url):
    try:
        async with aiohttp.request("GET", url) as resp:
            res = (await resp.json()).get("data", {}).get("card")
            if not res:
                return None, None
            card = json.loads(res["card"])
            dynamic_id = res["desc"]["dynamic_id"]
            vurl = f"https://t.bilibili.com/{dynamic_id}\n"
            item = card.get("item")
            if not item:
                return "动态不存在文字内容", vurl
            content = item.get("description")
            if not content:
                content = item.get("content")
            content = content.replace("\r", "\n")
            if len(content) > 250:
                content = content[:250] + "......"
            images = item.get("images")
            if images:
                images = [MessageSegment.image(i.get("img_src")) for i in images]
            else:
                images = []
            origin = card.get("origin")
            if origin:
                jorigin = json.loads(origin)
                short_link = jorigin.get("short_link")
                if short_link:
                    content += f"\n动态包含转发视频{short_link}"
                else:
                    content += f"\n动态包含转发其他动态"
            msg = Message(content)
            msg.extend(images)
            msg.append(vurl)
            return msg, vurl
    except Exception as e:
        logger.error(f"动态解析出错--Error:\n{e}")
        return "", ""
