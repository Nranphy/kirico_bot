from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
from kirico.utils.pic_utils import get_img
from .function import sign_in, sign_in_inquire



__kirico_plugin_name__ = '向雾子酱每日签到'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.2.2'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '雾子只想知道是否仍被在意呢...'

__kirico_plugin_usage__ = '''
每天可以发送指令【/签到】向雾子酱签到~可获得雾团子和好感度×
每天只能签到一次——嗯？不正常吗？
想查看签到状态的话可以用【/签到查询】哦~'''



__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True




sign_in_request = on_command("签到",aliases={"每日签到"}, priority = 7, block=True)

sign_in_information = on_command("签到信息",aliases={"签到统计","签到查询"}, priority = 7, block=True)




@sign_in_request.handle()
async def sign_in_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    feedback = await sign_in(qq)
    if feedback:
        await sign_in_request.finish("今日签到成功~\n"+MessageSegment.image(await get_img(f"http://q1.qlogo.cn/g?b=qq&nk={qq}&s=640"))+f"\n签到时间：{feedback[0]} {feedback[1]}\n连续签到：{feedback[3]} |签到总数：{feedback[2]}\n=====\n【好感度】增加{feedback[4][0]} |当前好感度为{feedback[4][1]}\n【雾团子】获得{feedback[5][0]} |当前数量 {feedback[5][1]}", at_sender = True)
    else:
        await sign_in_request.finish("签到失败...\n重复签到也是没用的！！口亨~", at_sender = True)


@sign_in_information.handle()
async def sign_in_inquire_process(bot:Bot, event:Event):
    qq = event.get_user_id()
    feedback = await sign_in_inquire(qq)
    if feedback:
        if_have_sign = "今日已签到√" if feedback[0] else "今日仍未签到哦...×"
        await sign_in_information.finish(f"查询成功~\n=========\n{if_have_sign}\n【上次签到时间】 {feedback[1]} {feedback[2]}\n【连续签到数】 {feedback[4]}\n【总签到次数】 {feedback[3]}\n=========\n继续加油哦~", at_sender = True)
    else:
        await sign_in_information.finish("查询失败...\n是否还未签过到呢×", at_sender = True)