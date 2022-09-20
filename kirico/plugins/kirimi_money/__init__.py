from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.log import logger
from kirico.utils.money_utils import money_inquire, money_change
from kirico.utils.file_utils import check_dir, check_file, get_date_and_time
import os
import json




__kirico_plugin_name__ = '雾团子货币'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.1.0'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '雾...雾团子...好次！！'

__kirico_plugin_usage__ = '''
和雾子酱互动、使用各种功能可以获得雾团子哦~
雾团子是像货币一样的东西、可在支持雾团子的各个系统使用~
雾团子查询【/查询雾团子】
===
cdk可使用【/cdk xxxx】进行兑换
'''


__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True




# 金钱查询
money_request = on_command("money", aliases={"查询雾团子", "查询金钱", "雾团子查询", "金钱查询"}, block=True)

@money_request.handle()
async def money_inquire_request(bot: Bot, event: Event, state: T_State = State()):
    qq = event.get_user_id()
    money_information = money_inquire(qq)
    msg = f"\n查询成功\n=========\n【当前雾团子】 {money_information[0]}\n=========\n"
    if money_information[1]:
        msg += "【变动记录】\n"
        for i in range(len(money_information[1])-1,-1,-1):
            temp = f"[{money_information[1][i][0]} {money_information[1][i][1]}] {money_information[1][i][2]} {money_information[1][i][3]:+}\n"
            msg += temp
    else:
        msg += "【暂无变动记录】\n"
    msg += "========="
    await money_request.finish(msg, at_sender=True)



# cdk兑换
cdk_exchange = on_command("cdk", aliases={"兑换码","激活码","礼品码","Cdk","CDK"}, priority=5, block=True)

@cdk_exchange.handle()
async def cdk_exchange_process(bot: Bot, event: Event, arg:Message = CommandArg(), state: T_State = State()):
    qq = event.get_user_id()
    cdk = arg.extract_plain_text()
    path = os.getcwd()+f"/kirico/data/cdk/{cdk}/"
    if os.path.isfile(path+f"{qq}"):
        await cdk_exchange.finish("你已兑换过此cdk~",at_sender = True)
    if not os.path.isfile(path+"cdk_setting.json"):
        await cdk_exchange.finish("此cdk不存在...请仔细检查哦",at_sender = True)
    with open(path+"cdk_setting.json","r") as f:
        cdk_data = json.load(f)
    if cdk_data["date"] < get_date_and_time()[0]:
        await cdk_exchange.finish("cdk已过期，无法兑换哦...",at_sender = True)
    info = money_change(qq,average=cdk_data["money"],note=f"使用了cdk【{cdk}】，获得了雾团子")
    check_file(path+f"{qq}")
    await cdk_exchange.finish(f"兑换成功~获得雾团子 {info[0]} 个\n【当前雾团子】{info[1]}",at_sender = True)
    


# cdk添加
cdk_setting = on_command("cdk添加", aliases={"添加cdk","添加Cdk","Cdk添加","CDK添加","添加CDK"}, priority=4, block=True, permission=SUPERUSER)

@cdk_setting.handle()
async def cdk_setting_process(bot: Bot, event: Event, arg:Message = CommandArg(), state: T_State = State()):
    command_ls = arg.extract_plain_text().strip().split()
    try:
        cdk = command_ls[0]
        money = int(command_ls[1])
    except:
        await cdk_setting.finish("cdk设置格式错误...请重新再试！！\n格式为【/cdk添加 cdk名 雾团子数 日期】",at_sender=True)
    try:
        date = command_ls[2]
    except:
        date = "9999-99-99"
    # date格式检查
    try:
        year = date[:4]
        month = date[5:7]
        day = date[8:10]
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            await cdk_setting.finish("日期格式设置格式错误...请重新再试！！\n格式为：yyyy-MM-dd",at_sender=True)
    except:
        await cdk_setting.finish("日期格式设置格式错误...请重新再试！！\n格式为：yyyy-MM-dd",at_sender=True)
    path = os.getcwd()+f"/kirico/data/cdk/{cdk}/"
    if not check_dir(path):
        await cdk_setting.finish("该cdk已存在，请更换cdk。")
    check_file(path+"cdk_setting.json")
    cdk_info = {"cdk":cdk, "money":money, "date":date}
    with open(path+"cdk_setting.json","w") as f:
        json.dump(cdk_info,f)
    await cdk_setting.finish("设置cdk成功！！",at_sender=True)




