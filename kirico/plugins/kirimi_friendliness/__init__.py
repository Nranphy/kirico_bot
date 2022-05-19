from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event
from kirico.utils.friendliness_utils import friendliness_inquire


__kirico_plugin_name__ = '雾子酱好感度~'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.2.0'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '雾子...dokidoki♡'

__kirico_plugin_usage__ = '''
和雾子酱互动、使用各种功能可以增加雾子酱的好感度哦~
===
好感度查询吧~【/查询好感度】
诶？想让雾子更换称呼？好感度超过200可使用【/设置称呼 xxx】来设定爱称√
雾子是群主的话还可以用【/设置头衔 xxx】来获取头衔哦~
===
通过每天不同时间的问候来增加雾子的好感度吧~
注意问候语要带上雾子关键词哦√
请不要一直重复问候雾子哦，雾子也是会厌烦的！！
不过，如果问候的时间错误的话...
另外，好感度超过一定值时雾子也会主动问好哦~
===
好感度到达一定程度可以和雾子交互哦...
请自行探索交互选项吧~
'''

__kirico__plugin_visible__ = True







# 好感度查询
friendliness_request = on_command("friendliness", aliases={"查询好感度", "查询好感", "好感度查询", "好感查询", "查好感"}, priority=7, block=True)



@friendliness_request.handle()
async def friendliness_inquire_request(bot: Bot, event: Event, state: T_State = State()):
    qq = event.get_user_id()
    friendliness_information = friendliness_inquire(qq)
    interactivity_data = get_interactivity_data(qq)

    msg = f"\n查询成功\n=========\n【当前好感度】 {friendliness_information[0]}\n=========\n"
    msg += "【交互统计】\n"+' | '.join([f"{get_transname(x)}雾子 {y}次" for x,y in interactivity_data.items()]) + "\n=========\n"
    if friendliness_information[1]:
        msg += "【变动记录】\n"
        for i in range(len(friendliness_information[1])-1,-1,-1):
            temp = f"[{friendliness_information[1][i][0]} {friendliness_information[1][i][1]}] {friendliness_information[1][i][2]} {friendliness_information[1][i][3]:+}\n"
            msg += temp
    else:
        msg += "【暂无变动记录】\n"
    msg += "========="
    await friendliness_request.finish(msg, at_sender=True)



# 设置别名
from .nickname import *


# 雾子酱问候
from .greetings import *

## 雾子自动问候
from .greetings_auto import *

# 雾子互动
from .interactivity import *