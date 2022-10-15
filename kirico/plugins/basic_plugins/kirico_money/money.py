from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

from kirico.utils.money_utils import KiricoMoney


# 金钱查询
money_request = on_command("money", aliases={"查询雾团子", "查询金钱", "雾团子查询", "金钱查询"}, block=True)

@money_request.handle()
async def money_inquire_request(bot: Bot, event: Event):
    qq = event.get_user_id()
    money_info = KiricoMoney(qq)
    await money_request.finish((
        "雾团子查询成功~\n"
        "=========\n"
        f"【当前雾团子】{money_info.count}\n"
        "=========\n"
        "【变动记录】\n"+
        ("暂无变动记录" if not money_info.change_log else "\n".join([f"[{log[0]} {log[1]}] {log[2]} {log[3]:+}" for log in money_info.change_log]))+"\n"
        "========="
    ), at_sender=True)