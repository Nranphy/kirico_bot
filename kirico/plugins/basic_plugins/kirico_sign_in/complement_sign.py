from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

from kirico.utils.friendliness_utils import KiricoFriendliness
from kirico.utils.money_utils import KiricoMoney

from .utils import KiricoSigninData



complement_sign = on_command("补签", priority = 7, block=True)



@complement_sign.handle()
async def complement_sign_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    sign_in = KiricoSigninData(qq)
    # result = sign_in.sign()
    # if result:
    #     #好感度变化
    #     friendliness_info = KiricoFriendliness(qq)
    #     friendliness = friendliness_info.change(30, 10, note = "签到成功，获得好感值")
    #     #金币变化
    #     money_info = KiricoMoney(qq)
    #     money = money_info.change(2000, 1500, note = "签到成功，获得雾团子")
    #     await complement_sign.finish((
    #         "今日签到成功~\n"
    #         "=========\n"
    #         f"签到时间：{sign_in.now_date.date} {sign_in.now_date.time}\n"
    #         f"连续签到：{sign_in.today_continuous_days()} | 签到总数：{sign_in.total_days} | 最大连续签到数：{sign_in.max_continuous_days}\n"
    #         "=====\n"
    #         f"【好感度】增加{friendliness[0]} |当前好感度为{friendliness[1]}\n"
    #         f"【雾团子】获得{money[0]} |当前数量 {money[1]}"
    #     ), at_sender = True)
    # else:
    #     await complement_sign_process.finish("签到失败...\n不可以重复签到哦~！！", at_sender = True)