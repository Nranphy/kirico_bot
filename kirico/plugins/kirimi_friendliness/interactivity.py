from nonebot import on_command, get_bot, get_driver, on_regex
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
from kirico.utils.friendliness_utils import friendliness_inquire, friendliness_change, get_nickname
from kirico.utils.file_utils import get_date_and_time, check_dir, check_file
import random
import os
import json



touch = on_regex(pattern=".*?摸.{0,5}?雾子.*?|.*?雾子.{0,5}?摸.*?", priority=12, block=True)

tete = on_regex(pattern=".*?贴.{0,5}?雾子.*?|.*?雾子.{0,5}?贴.*?", priority=13, block=True)

kiss = on_regex(pattern=".*?(亲|啾|mua).{0,5}?雾子.*?|.*?雾子.{0,5}?(亲|啾|mua).*?", priority=14, block=True)


dirty = on_regex(pattern=".*?(爬|爪巴|滚|傻逼|弱智|脑残|脑瘫|脑弹|智障|废物|fw|垃圾|烧鸡).{0,5}?雾子.*?|.*?雾子.{0,5}?(爬|爪巴|滚|傻逼|弱智|脑残|脑瘫|脑弹|智障|废物|fw|垃圾|烧鸡).*?", priority=15, block=True)

papa = on_regex(pattern=".*?(肛|日|啪|透|草|超市|茶包|炒饭|铜丝|橄榄).{0,5}?雾子.*?|.*?雾子.{0,5}?(肛|日|啪|透|草|超市|茶包|炒饭|铜丝|橄榄).*?", priority=16, block=True)




@touch.handle()
async def touch_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    friendliness = friendliness_inquire(qq)[0]
    date_time = get_date_and_time()
    # 好感度判定
    if friendliness<0:
        ls = [
            "雾子...还要再亲近一点才行哦×",
            "果咩...雾子还不是很信任你呢...",
            "不...不行的哦（推开）"
        ]
        friendliness_change(qq,5,10,note="想要摸摸雾子，但是被拒绝了...")
        await touch.finish(random.choice(ls),at_sender=True)
    # 冷却判定
    cache_path = os.getcwd()+"/data/interactivity_cache/touch.json"
    check_dir(os.getcwd()+"/data/interactivity_cache/")
    check_file(cache_path)
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    if json_data.get(qq,dict()).get("date","") == date_time[0] and abs(int(json_data.get(qq,dict()).get("time","99:99:99")[:2]) - int(date_time[1][:2]))<2:
        ls = [
            "摸摸太多次了啦...！",
            "等..等会再来吧（逃）",
            "头发...头发乱掉了啦×",
            "再摸摸雾子可就不理你了！！（口亨）"]
        await touch.finish(random.choice(ls),at_sender=True)
    
    # 通过判定
    friendliness_change(qq,10,10,note="摸摸雾子~好感度增加了")
    ## 记录冷却
    json_data[qq] = {"date":date_time[0],"time":date_time[1]}
    try:
        with open(cache_path,"w") as f:
            json.dump(json_data,f)
    except:
        pass
    ## 记录次数
    record_path = os.getcwd()+f"/kirico/data/friendliness/interactivity/{qq}.json"
    check_dir(os.getcwd()+"/kirico/data/friendliness/interactivity/")
    check_file(record_path)
    try:
        with open(record_path,"r") as f:
            record_data = json.load(f)
    except:
        record_data = dict()
    record_data["touch"] = record_data.get("touch",0) + 1
    try:
        with open(record_path,"w") as f:
            json.dump(record_data,f)
    except:
        await touch.send("记录失败呢...",at_sender=True)
    ## 正式回复
    ### 别名引入
    nickname = get_nickname(qq)

    ls = [
        f"{nickname}的手掌...好温暖♡",
        f"{nickname}...以后也可以这样摸摸雾子吗~？",
        f"...心里总有种暖暖的感觉呢...{nickname}♡"
        ]
    await touch.finish(random.choice(ls),at_sender=True)



@tete.handle()
async def tete_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    friendliness = friendliness_inquire(qq)[0]
    date_time = get_date_and_time()
    # 好感度判定
    if friendliness<50:
        ls = [
            "雾子...还要再亲近一点才行哦×",
            "果咩...雾子还不是很信任你呢...",
            "不...不行的哦（推开）"
        ]
        friendliness_change(qq,5,10,note="想要贴贴雾子，但是被拒绝了...")
        await tete.finish(random.choice(ls),at_sender=True)
    # 冷却判定
    cache_path = os.getcwd()+"/data/interactivity_cache/tete.json"
    check_dir(os.getcwd()+"/data/interactivity_cache/")
    check_file(cache_path)
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    if json_data.get(qq,dict()).get("date","") == date_time[0] and abs(int(json_data.get(qq,dict()).get("time","99:99:99")[:2]) - int(date_time[1][:2]))<2:
        ls = [
            "贴贴太久了啦...！",
            "等..等会再来吧（逃）",
            "贴贴太紧了...有点难为情呢×"]
        await tete.finish(random.choice(ls),at_sender=True)
    
    # 通过判定
    friendliness_change(qq,10,10,note="贴贴雾子~好感度增加了")
    ## 记录冷却
    json_data[qq] = {"date":date_time[0],"time":date_time[1]}
    try:
        with open(cache_path,"w") as f:
            json.dump(json_data,f)
    except:
        pass
    ## 记录次数
    record_path = os.getcwd()+f"/kirico/data/friendliness/interactivity/{qq}.json"
    check_dir(os.getcwd()+"/kirico/data/friendliness/interactivity/")
    check_file(record_path)
    try:
        with open(record_path,"r") as f:
            record_data = json.load(f)
    except:
        record_data = dict()
    record_data["tete"] = record_data.get("tete",0) + 1
    try:
        with open(record_path,"w") as f:
            json.dump(record_data,f)
    except:
        await tete.send("记录失败呢...",at_sender=True)
    ## 正式回复
    ### 别名引入
    nickname = get_nickname(qq)

    ls = [
        f"贴贴贴贴{nickname}...♡",
        f"{nickname}...爱你哦~♡",
        f"心里总有种暖暖的感觉呢...{nickname}♡"
        ]
    await tete.finish(random.choice(ls),at_sender=True)


@kiss.handle()
async def kiss_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    friendliness = friendliness_inquire(qq)[0]
    date_time = get_date_and_time()
    # 好感度判定
    if friendliness<200:
        ls = [
            "雾子...还要再亲近一点才行哦×",
            "果咩...雾子还不是很信任你呢...",
            "不...不行的哦（推开）",
            "唔...雾子...会害羞的！"
        ]
        friendliness_change(qq,5,10,note="想要亲亲雾子，但是被拒绝了...")
        await kiss.finish(random.choice(ls),at_sender=True)
    # 冷却判定
    cache_path = os.getcwd()+"/data/interactivity_cache/kiss.json"
    check_dir(os.getcwd()+"/data/interactivity_cache/")
    check_file(cache_path)
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    if json_data.get(qq,dict()).get("date","") == date_time[0] and abs(int(json_data.get(qq,dict()).get("time","99:99:99")[:2]) - int(date_time[1][:2]))<2:
        ls = [
            "诶？还要亲亲吗",
            "亲亲太多次了啦（逃）",
            "让...雾子休息一下吧×"]
        await kiss.finish(random.choice(ls),at_sender=True)
    
    # 通过判定
    friendliness_change(qq,10,10,note="亲亲雾子~好感度增加了")
    ## 记录冷却
    json_data[qq] = {"date":date_time[0],"time":date_time[1]}
    try:
        with open(cache_path,"w") as f:
            json.dump(json_data,f)
    except:
        pass
    ## 记录次数
    record_path = os.getcwd()+f"/kirico/data/friendliness/interactivity/{qq}.json"
    check_dir(os.getcwd()+"/kirico/data/friendliness/interactivity/")
    check_file(record_path)
    try:
        with open(record_path,"r") as f:
            record_data = json.load(f)
    except:
        record_data = dict()
    record_data["kiss"] = record_data.get("kiss",0) + 1
    try:
        with open(record_path,"w") as f:
            json.dump(record_data,f)
    except:
        await kiss.send("记录失败呢...",at_sender=True)
    ## 正式回复
    ### 别名引入
    nickname = get_nickname(qq)

    ls = [
        f"啾啾{nickname}...爱你哦♡",
        f"亲亲{nickname}...总感觉有点害羞呢~♡",
        f"亲亲{nickname}...雾子好像有点奇怪了...♡"
        ]
    await kiss.finish(random.choice(ls),at_sender=True)


@dirty.handle()
async def dirty_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    friendliness = friendliness_inquire(qq)[0]
    date_time = get_date_and_time()
    friendliness_change(qq,-20,10,note="骂了雾子...")
    if random.random() > 0.5:
        await dirty.finish()
    ls = ["雾子...被骂了","...讨厌鬼","雾子不会再和你说话了...！！","呜呜...被骂了..."]
    await dirty.finish(random.choice(ls),at_sender=True)


@papa.handle()
async def papa_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    friendliness = friendliness_inquire(qq)[0]
    date_time = get_date_and_time()
    # 好感度判定
    if friendliness<5000:
        ls = [
            "笨...笨蛋！！！！！才不行呢！",
            "这种事情...怎么想都很奇怪吧...×",
            "不...不行的哦（推开）",
            "雾子...才不要呢！！"
        ]
        friendliness_change(qq,-20,10,note="想要啪啪雾子，但是被拒绝了...")
        await papa.finish(random.choice(ls),at_sender=True)
    # 冷却判定
    cache_path = os.getcwd()+"/data/interactivity_cache/papa.json"
    check_dir(os.getcwd()+"/data/interactivity_cache/")
    check_file(cache_path)
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    if json_data.get(qq,dict()).get("date","") == date_time[0] and abs(int(json_data.get(qq,dict()).get("time","99:99:99")[:2]) - int(date_time[1][:2]))<2:
        ls = [
            "...（没有回应）",
            "雾子酱...想休息呢...",
            "不...不行呢..."]
        await papa.finish(random.choice(ls),at_sender=True)
    # 啪啪概率判定
    if random.random() < 0.5:
        ls = [
            "抱歉...今天不行哦...",
            "笨蛋× 下次吧...（小声",
            "诶...让雾子考虑一下可以吗..."
        ]
        await papa.finish(random.choice(ls),at_sender=True)
    
    # 通过判定
    friendliness_change(qq,30,20,note="啪啪雾子~好感度增加了")
    ## 记录冷却
    json_data[qq] = {"date":date_time[0],"time":date_time[1]}
    try:
        with open(cache_path,"w") as f:
            json.dump(json_data,f)
    except:
        pass
    ## 记录次数
    record_path = os.getcwd()+f"/kirico/data/friendliness/interactivity/{qq}.json"
    check_dir(os.getcwd()+"/kirico/data/friendliness/interactivity/")
    check_file(record_path)
    try:
        with open(record_path,"r") as f:
            record_data = json.load(f)
    except:
        record_data = dict()
    record_data["papa"] = record_data.get("papa",0) + 1
    try:
        with open(record_path,"w") as f:
            json.dump(record_data,f)
    except:
        await papa.send("记录失败呢...",at_sender=True)
    ## 正式回复
    ### 别名引入
    nickname = get_nickname(qq)

    ls = [
        f"{nickname}...爱你♡",
        f"...总感觉有点害羞呢...{nickname}，爱你♡",
        f"...雾子...变得奇怪了...——{nickname}♡"
        ]
    await papa.finish(random.choice(ls),at_sender=True)