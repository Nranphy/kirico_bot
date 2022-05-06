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




# __kirico_plugin_name__ = '雾子酱问候~'

# __kirico_plugin_author__ = 'Nranphy'

# __kirico_plugin_version__ = '0.0.8'

# __kirico_plugin_repositorie__ = ''

# __kirico_plugin_description__ = '早安哦~米娜桑~☆'

# __kirico_plugin_usage__ = '''
# 通过每天不同时间的问候来增加雾子的好感度吧~
# 注意问候语要带上雾子关键词哦√
# 请不要一直重复问候雾子哦
# 另外，如果问候的时间错误的话...
# '''


# __kirico__plugin_visible__ = True








# 对雾子的日常问候

morning = on_regex(pattern=".*?(早啊|早哦|早捏|早安|早上好|上午好).*?雾子.*?|.*?雾子.*?(早啊|早哦|早捏|早安|早上好|上午好).*?", priority=7, block=True)

midday = on_regex(pattern=".*?(中午好|午安).*?雾子.*?|.*?雾子.*?(中午好|午安).*?", priority=7, block=True)

afternoon = on_regex(pattern=".*?下午好.*?雾子.*?|.*?雾子.*?下午好.*?", priority=7, block=True)

evening = on_regex(pattern=".*?(晚好|晚上好).*?雾子.*?|.*?雾子.*?(晚好|晚上好).*?", priority=7, block=True)

night = on_regex(pattern=".*?(晚安|好梦|睡了|睡觉了).*?雾子.*?|.*?雾子.*?(晚安|好梦|睡了|睡觉了).*?", priority=7, block=True)


@morning.handle()
async def morning_greeting(bot:Bot, event:Event):
    qq = event.get_user_id()
    nickname = get_nickname(qq)

    cache_path = os.getcwd()+"/data/greetings_cache.json"
    check_dir(os.getcwd()+"/data/")
    check_file(os.getcwd()+"/data/greetings_cache.json")
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    last_date = json_data.get(qq,[0,0,0])[0]
    last_hour = json_data.get(qq,[0,0,0])[1]
    last_minute = json_data.get(qq,[0,0,0])[2]

    date_time_ls = get_date_and_time()
    date = date_time_ls[0]
    hour = int(date_time_ls[1][:2])
    minute = int(date_time_ls[1][3:5])
    if date == last_date and hour == last_hour and abs(minute-last_minute) <=2: # 简单地使用靠日期和小时数来达成冷却
        ls = [
            f"诶？{nickname}不是刚问候过的吗...",
            "知道啦知道啦...！！",
            "真是的...",
            "唔...嗯！",
            f"{nickname}再一直问候下去，雾子可就不理你了！！",
            "口亨~",
            "还在问候...七秒钟的记忆已经消失了吗？（疑惑...）"
        ]
        await morning.finish(random.choice(ls), at_sender=True)
    elif 0<= hour < 5:
        ls = [
            "早...早安？",
            "早安...？虽然雾子不会困就是了...",
            f"{nickname}早安得太早了啦！！",
            "太早的早安会打扰到其他人哦..."
        ]
        friendliness_change(qq,-5,10,note="给雾子说了早安，但是弄错了时间...")
        await morning.send(random.choice(ls), at_sender=True)
    elif 5<= hour <11:
        ls = [
            "早安哦~ 今天也是充满希望的一天√",
            f"早安ww {nickname}昨晚有做好梦吗？",
            f"早~ {nickname}今天要干什么呢~"
        ]
        friendliness_change(qq,20,5,note="给雾子说了早安√")
        await morning.send(random.choice(ls), at_sender=True)
    elif 11<= hour <21:
        ls = [
            "这个时候吗...×",
            f"{nickname}现在起床也太晚啦———太·晚·啦！！",
            "现在才起床的话...好懒哦×"
        ]
        friendliness_change(qq,-5,10,note="给雾子说了早安，但是弄错了时间...")
        await morning.send(random.choice(ls), at_sender=True)
    else:
        ls = [
            "早...？",
            "早×你是从另一个世界来的吗×",
            f"{nickname}早安哦~诶、莫不是用错了九宫格——",
        ]
        friendliness_change(qq,-5,10,note="给雾子说了早安，但是弄错了时间...")
        await morning.send(random.choice(ls), at_sender=True)

    json_data[qq] = [date, hour, minute]
    with open(cache_path,'w+') as f:
        json.dump(json_data, f)


    
@midday.handle()
async def midday_greeting(bot:Bot, event:Event):
    qq = event.get_user_id()
    nickname = get_nickname(qq)

    cache_path = os.getcwd()+"/data/greetings_cache.json"
    check_dir(os.getcwd()+"/data/")
    check_file(os.getcwd()+"/data/greetings_cache.json")
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    last_date = json_data.get(qq,[0,0,0])[0]
    last_hour = json_data.get(qq,[0,0,0])[1]
    last_minute = json_data.get(qq,[0,0,0])[2]

    date_time_ls = get_date_and_time()
    date = date_time_ls[0]
    hour = int(date_time_ls[1][:2])
    minute = int(date_time_ls[1][3:5])
    if date == last_date and hour == last_hour and abs(minute-last_minute) <=2: # 简单地使用靠日期和小时数来达成冷却
        ls = [
            f"诶？{nickname}不是刚问候过的吗...",
            "知道啦知道啦...！！",
            "真是的...",
            "唔...嗯！",
            f"{nickname}再一直问候下去，雾子可就不理你了！！",
            "口亨~",
            "还在问候...七秒钟的记忆已经消失了吗？"
        ]
        await midday.finish(random.choice(ls), at_sender=True)
    elif 6<= hour < 11:
        ls = [
            "现在说午安也太早啦×",
            "距离中午还有段时间哦...",
            "正在思考中午要吃什么呢..."
        ]
        friendliness_change(qq,-5,10,note="给雾子说了午安，但是弄错了时间...")
        await midday.send(random.choice(ls), at_sender=True)
    elif 11<= hour <14:
        ls = [
            f"{nickname}中午好哦~有在好好吃饭吗~",
            "中午好ww 今中午吃的什么呢~",
            f"{nickname}午好~ 休息一下吧~"
        ]
        friendliness_change(qq,15,5,note="给雾子说了午安√")
        await midday.send(random.choice(ls), at_sender=True)
    elif 14<= hour <20:
        ls = [
            "现在说午好也太迟了啦！！",
            "那个...已经不是中午了哦~"
        ]
        friendliness_change(qq,-5,10,note="给雾子说了午安，但是弄错了时间...")
        await midday.send(random.choice(ls), at_sender=True)
    else:
        ls = [
            "嗯...嗯？",
            "诶？现在...是中午吗（疑惑）"
        ]
        friendliness_change(qq,-5,10,note="给雾子说了午安，但是弄错了时间...")
        await midday.send(random.choice(ls), at_sender=True)
        

    json_data[qq] = [date, hour, minute]
    with open(cache_path,'w+') as f:
        json.dump(json_data, f)
    
@afternoon.handle()
async def afternoon_greeting(bot:Bot, event:Event):
    qq = event.get_user_id()
    nickname = get_nickname(qq)

    cache_path = os.getcwd()+"/data/greetings_cache.json"
    check_dir(os.getcwd()+"/data/")
    check_file(os.getcwd()+"/data/greetings_cache.json")
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    last_date = json_data.get(qq,[0,0,0])[0]
    last_hour = json_data.get(qq,[0,0,0])[1]
    last_minute = json_data.get(qq,[0,0,0])[2]

    date_time_ls = get_date_and_time()
    date = date_time_ls[0]
    hour = int(date_time_ls[1][:2])
    minute = int(date_time_ls[1][3:5])
    if date == last_date and hour == last_hour and abs(minute-last_minute) <=2: # 简单地使用靠日期和小时数来达成冷却
        ls = [
            f"诶？{nickname}不是刚问候过的吗...",
            "知道啦知道啦...！！",
            "真是的...",
            "唔...嗯！",
            f"{nickname}再一直问候下去，雾子可就不理你了！！",
            "口亨~",
            "还在问候...七秒钟的记忆已经消失了吗？"
        ]
        await afternoon.finish(random.choice(ls), at_sender=True)
    elif 6<= hour < 11:
        ls = [
            "说早安哦~早——安——！",
            "现在才不是下午哦×",
            "雾子不会记错时间的！雾子很聪明！"
        ]
        friendliness_change(qq,-5,10,note="给雾子说了下午好，但是弄错了时间...")
        await afternoon.send(random.choice(ls), at_sender=True)
    elif 11<= hour <13:
        ls = [
            "距离下午还有段时间哦...",
            f"{nickname}快给雾子说中午好！！",
            "时间好像记错了哦..."
        ]
        friendliness_change(qq,-5,10,note="给雾子说了下午好，但是弄错了时间...")
        await afternoon.send(random.choice(ls), at_sender=True)
    elif 13<= hour <18:
        ls = [
            f"{nickname}下午好哦~下午要干什么呢~",
            f"{nickname}下午好~要和雾子一起喝下午茶吗~",
            f"{nickname}下午好ww 今晚吃什么呢——"
        ]
        friendliness_change(qq,15,5,note="给雾子说了下午好√")
        await afternoon.send(random.choice(ls), at_sender=True)
    else:
        ls = [
            f"“下午好”得太晚了啦——{nickname}",
            "现在可不是下午哦...",
            "真是的...雾子都要睡着啦..."
        ]
        friendliness_change(qq,-5,10,note="给雾子说了下午好，但是弄错了时间...")
        await afternoon.send(random.choice(ls), at_sender=True)

    json_data[qq] = [date, hour, minute]
    with open(cache_path,'w+') as f:
        json.dump(json_data, f)
    

@evening.handle()
async def evening_greeting(bot:Bot, event:Event):
    qq = event.get_user_id()
    nickname = get_nickname(qq)

    cache_path = os.getcwd()+"/data/greetings_cache.json"
    check_dir(os.getcwd()+"/data/")
    check_file(os.getcwd()+"/data/greetings_cache.json")
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    last_date = json_data.get(qq,[0,0,0])[0]
    last_hour = json_data.get(qq,[0,0,0])[1]
    last_minute = json_data.get(qq,[0,0,0])[2]

    date_time_ls = get_date_and_time()
    date = date_time_ls[0]
    hour = int(date_time_ls[1][:2])
    minute = int(date_time_ls[1][3:5])
    if date == last_date and hour == last_hour and abs(minute-last_minute) <=2: # 简单地使用靠日期和小时数来达成冷却
        ls = [
            f"诶？{nickname}不是刚问候过的吗...",
            "知道啦知道啦...！！",
            "真是的...",
            "唔...嗯！",
            f"{nickname}再一直问候下去，雾子可就不理你了！！",
            "口亨~",
            "还在问候...七秒钟的记忆已经消失了吗？"
        ]
        await evening.finish(random.choice(ls), at_sender=True)
    elif 6<= hour < 10:
        ls = [
            "现在才不是晚上呢！！",
            f"{nickname}该醒啦！！",
            "夜晚已经过去了哦..."
        ]
        friendliness_change(qq,-5,10,note="给雾子说了晚上好，但是弄错了时间...")
        await evening.send(random.choice(ls), at_sender=True)
    elif 10<= hour <18:
        ls = [
            "距离晚上还有点时间哦...",
            "再过一会才是晚上啦！！",
            "雾子这里的天还没黑下来哦..."
        ]
        friendliness_change(qq,-5,10,note="给雾子说了晚上好，但是弄错了时间...")
        await evening.send(random.choice(ls), at_sender=True)
    else:
        ls = [
            f"{nickname}晚好哦~稍稍休息吧~",
            f"{nickname}晚上好哦~今天还算开心吗~",
            f"{nickname}晚上好√ 今晚要早点睡哦~"
        ]
        friendliness_change(qq,20,10,note="给雾子说了晚上好√")
        await evening.send(random.choice(ls), at_sender=True)

    json_data[qq] = [date, hour, minute]
    with open(cache_path,'w+') as f:
        json.dump(json_data, f)
    
@night.handle()
async def night_greeting(bot:Bot, event:Event):
    qq = event.get_user_id()
    nickname = get_nickname(qq)

    cache_path = os.getcwd()+"/data/greetings_cache.json"
    check_dir(os.getcwd()+"/data/")
    check_file(os.getcwd()+"/data/greetings_cache.json")
    try:
        with open(cache_path,'r') as f:
            json_data = json.load(f)
    except:
        json_data = dict()
    last_date = json_data.get(qq,[0,0,0])[0]
    last_hour = json_data.get(qq,[0,0,0])[1]
    last_minute = json_data.get(qq,[0,0,0])[2]

    date_time_ls = get_date_and_time()
    date = date_time_ls[0]
    hour = int(date_time_ls[1][:2])
    minute = int(date_time_ls[1][3:5])
    if date == last_date and hour == last_hour and abs(minute-last_minute) <=2: # 简单地使用靠日期和小时数来达成冷却
        ls = [
            f"诶？{nickname}不是刚问候过的吗...",
            "知道啦知道啦...！！",
            "真是的...",
            "唔...嗯！",
            f"{nickname}再一直问候下去，雾子可就不理你了！！",
            "口亨~",
            "还在问候...七秒钟的记忆已经消失了吗？"
        ]
        await night.finish(random.choice(ls), at_sender=True)
    elif 2<= hour < 8:
        ls = [
            f"晚安——{nickname}睡得太迟了哦...",
            "已经快天亮了...快睡吧~",
            f"晚安...{nickname}下次可不要睡这么晚了哦"
        ]
        friendliness_change(qq,0,10,note="给雾子说了晚安，但好像睡得太晚了...")
        await night.send(random.choice(ls), at_sender=True)
    elif 8<= hour <19:
        ls = [
            "诶？现在就要睡觉了吗——",
            "晚a——现在可是白天哦？",
            "你是来调戏雾子的吧！！一定是的吧！！",
            f"{nickname}还不能睡觉哦~白天的工作做完了吗~"
        ]
        friendliness_change(qq,-5,10,note="给雾子说了晚安，但是弄错了时间...")
        await night.send(random.choice(ls), at_sender=True)
    elif 19<= hour <21:
        ls = [
            f"{nickname}晚安...睡的真早呢...",
            f"{nickname}晚安~ 这个时候睡应该不会睡懒觉吧×",
            f"{nickname}晚安ww 明明夜晚才刚开始呢..."
        ]
        friendliness_change(qq,0,10,note="给雾子说了晚安，但好像睡得有点早...")
        await night.send(random.choice(ls), at_sender=True)
    else:
        ls = [
            "晚安哦~今晚会梦到雾子吗~",
            f"晚安！！{nickname}一定会做个好梦的哦~",
            "晚安~ 需要雾子给你唱安眠曲吗~",
            f"晚安√ {nickname}明天再见哦~"
        ]
        friendliness_change(qq,20,10,note="给雾子说了晚安√")
        await night.send(random.choice(ls), at_sender=True)

    json_data[qq] = [date, hour, minute]
    with open(cache_path,'w+') as f:
        json.dump(json_data, f)