from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

from utils.friendliness_utils import KiricoFriendliness

from .util import get_interactivity_data, get_transname



# 好感度查询
friendliness_request = on_command("friendliness", aliases={"查询好感度", "查询好感", "好感度查询", "好感查询", "查好感"}, priority=7, block=True)



@friendliness_request.handle()
async def friendliness_inquire_request(bot: Bot, event: Event):
    qq = event.get_user_id()
    friendliness_info = KiricoFriendliness(qq)
    interactivity_data = get_interactivity_data(qq)

    await friendliness_request.finish((
        "好感度查询成功~\n"
        "=========\n"
        f"【当前好感度】{friendliness_info.count}\n"
        "=========\n"
        "【交互统计】\n"+
        (' | '.join([f"{get_transname(x)}雾子{y}次" for x,y in interactivity_data.items()]) +'\n')+
        "=========\n"
        "【变动记录】\n"+
        ("暂无变动记录" if not friendliness_info.change_log else '\n'.join([f"[{log[0]} {log[1]}] {log[2]} {log[3]:+}" for log in friendliness_info.change_log])) +'\n'
        "========="
    ), at_sender=True)