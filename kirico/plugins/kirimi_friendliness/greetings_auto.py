from nonebot import on_command, get_bot, get_driver, on_message, on_regex
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
from kirico.utils.friendliness_utils import friendliness_inquire, friendliness_change, get_nickname
from kirico.utils.file_utils import get_date_and_time, check_dir, check_file

import random
import os
import json






auto_greeting = on_regex(pattern=".*?(早啊|早哦|早捏|早安|早上好|上午好|午安|午好|晚好|晚安|晚上好|睡了|碎了|睡觉了|寝了).*?", priority=15)

@auto_greeting.handle()
async def auto_greeting_process(bot:Bot, event:Event):
    # 好感度判定
    friendliness = friendliness_inquire(event.get_user_id())[0]
    if friendliness<500: 
        await auto_greeting.finish()

    # 次数判定
    date_time = get_date_and_time()
    hour = int(date_time[1][:2])
    cache_path = os.getcwd()+"/data/greetings_auto_cache.json"
    check_dir(os.getcwd()+"/data/")
    check_file(os.getcwd()+"/data/greetings_auto_cache.json")
    try:
        with open(cache_path,"r") as f:
            data = json.load(f)
    except:
        data = dict()
    if data.get(event.get_user_id(),dict()).get("date","") == date_time[0] and abs(int(data.get(event.get_user_id(),dict()).get("time","99:99:99")[:2]) - int(date_time[1][:2])) <=2:
        await auto_greeting.finish()

    # 概率判断
    if random.random()<=0.2:
        await auto_greeting.finish()
    
    # 通过检测，可以回复。
    data[event.get_user_id()]["date"] = date_time[0]
    data[event.get_user_id()]["time"] = date_time[1]
    try:
        with open(cache_path,"w") as f:
            json.dump(data,f)
    except:
        pass
    ## nickname加入
    nickname = get_nickname(event.get_user_id())

    if 0<=hour<=3 or 23<=hour<=24:
        ls = [
            f"{nickname}要睡觉了吗~？雾子想对你说晚安哦~",
            f"晚安呢~{nickname}今天一定会做个好梦的吧~",
            f"要睡觉了吗？{nickname}今晚会不会梦见雾子呢~"
        ] #晚安
        await auto_greeting.finish(random.choice(ls),at_sender=True)
    elif 4<=hour<=10:
        ls = [
            f"早...早安哦~{nickname}（打哈欠",
            f"{nickname}早安！昨晚睡得还好吗~",
            f"{nickname}早上好哦~"
        ] #早安
        await auto_greeting.finish(random.choice(ls),at_sender=True)
    elif 11<=hour<=13:
        ls = [
            f"中午好呢！{nickname}~",
            f"中午了哦~{nickname}午好！！",
            f"{nickname}中午好哦~"
        ] #中午好
        await auto_greeting.finish(random.choice(ls),at_sender=True)
    elif 14<=hour<=17:
        ls = [
            f"{nickname}下午好~",
            f"下午出没...{nickname}又在摸鱼吗（口亨~",
            f"{nickname}要来一杯下午茶吗~"
        ] #下午好
        await auto_greeting.finish(random.choice(ls),at_sender=True)
    else:
        ls = [
            f"{nickname}晚上好！！",
            f"欢迎回来~{nickname} 已经是晚上了哦~",
            f"晚上好唷~{nickname}"
        ] #晚上好
        await auto_greeting.finish(random.choice(ls),at_sender=True)