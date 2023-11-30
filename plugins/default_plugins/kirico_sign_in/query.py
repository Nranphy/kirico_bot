from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

from utils.friendliness_utils import KiricoFriendliness
from utils.money_utils import KiricoMoney

from .utils import KiricoSigninData



sign_in_information = on_command("签到信息",aliases={"签到统计","签到查询","查询签到"}, priority = 6, block=True)



@sign_in_information.handle()
async def sign_in_inquire_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    sign_in = KiricoSigninData(qq)
    missing_days = ','.join([str(day) for day in range(1,sign_in.now_date.day) if not sign_in.sign_in_status[day]])
    await sign_in_information.finish((
        "签到信息查询成功~\n"
        "=========\n"+
        ("今日已签到√\n" if sign_in.today_have_sign() else "今日还未签到哦...\n")+
        f"【上次签到时间】{sign_in.last_date}\n"
        f"【连续签到数】{sign_in.today_continuous_days()} | 【最大连续签到数】{sign_in.max_continuous_days}\n"
        f"【签到总次数】{sign_in.total_days}\n"
        f"【补签次数】{sign_in.complement}\n"
        "=========\n"
        f"{'【本月可补签日期】'+missing_days if missing_days else ''}\n=========\n"
        "要继续加油哦~"
    ), at_sender = True)