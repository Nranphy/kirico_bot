from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Event, Message

from utils.money_utils import KiricoMoney
from utils.file_utils import load_data, save_data
from utils.basic_utils import check_format_date, KiricoDatetime


cdk_exchange = on_command("cdk", aliases={"兑换码","激活码","礼品码","Cdk","CDK"}, priority=5, block=True)

cdk_setting = on_command("cdk添加", aliases={"添加cdk","添加Cdk","Cdk添加","CDK添加","添加CDK"}, priority=4, block=True, permission=SUPERUSER)



_cdk_data_pathname = "cdk"


# cdk兑换

@cdk_exchange.handle()
async def cdk_exchange_process(bot: Bot, event: Event, arg:Message = CommandArg()):
    qq = event.get_user_id()
    cdk = arg.extract_plain_text().strip()

    all_cdk_data = load_data(_cdk_data_pathname, "all_cdk")
    if cdk not in all_cdk_data["data"]:
        await cdk_exchange.finish("此CDK不存在哦...请再检查一下吧~", at_sender = True)

    target_cdk_data = load_data(_cdk_data_pathname, cdk)
    if qq in target_cdk_data["exchanged"]:
        await cdk_exchange.finish("你已经兑换过此CDK了！！",at_sender = True)
    
    now_date = KiricoDatetime()
    if now_date.date > target_cdk_data["date"]:
        await cdk_exchange.finish(f"该CDK已经过期了哦...\n【过期时间】{target_cdk_data['date']}",at_sender = True)
    
    money_info = KiricoMoney(qq)
    money_info.change(target_cdk_data["money"], 0, f"使用了CDK【{cdk}】")

    target_cdk_data["exchanged"].append(str(qq))
    save_data(_cdk_data_pathname, cdk, target_cdk_data)
    await cdk_exchange.finish((
        f"兑换成功~获得雾团子 {target_cdk_data['money']} 个\n"
        f"【当前雾团子】{money_info.count}"),at_sender = True)
    


# cdk添加

@cdk_setting.handle()
async def cdk_setting_process(bot: Bot, event: Event, arg:Message = CommandArg()):
    '''指令格式为 /cdk添加 cdk名 雾团子数 日期'''
    command_ls = arg.extract_plain_text().strip().split()
    if not command_ls:
        await cdk_setting.finish((
            "该指令可添加CDK兑换码√\n"
            "【指令格式】/cdk添加 cdk名 雾团子数 日期\n"
            "其中，日期要为标准格式，如1970-01-01"), at_sender=True)

    if len(command_ls)<3:
        await cdk_setting.finish((
            "指令格式错误...\n"
            "=========\n"
            "【指令格式】/cdk添加 cdk名 雾团子数 日期\n"
            "其中，日期要为标准格式，如1970-01-01，注意前导0哦..."
        ), at_sender=True)
    
    cdk = command_ls[0]

    if command_ls[1].isdigit():
        money = int(command_ls[1])
    else:
        await cdk_setting.finish((
            "雾团子数不为数字哦...\n"
            "=========\n"
            "【指令格式】/cdk添加 cdk名 雾团子数 日期\n"
            "其中，日期要为标准格式，如1970-01-01"
        ), at_sender=True)
    
    if check_format_date(command_ls[2]):
        date = command_ls[2]
    else:
        await cdk_setting.finish((
            "日期不为标准时间...\n"
            "=========\n"
            "【指令格式】/cdk添加 cdk名 雾团子数 日期\n"
            "其中，日期要为标准格式，如1970-01-01"
        ), at_sender=True)

    all_cdk_data = load_data(_cdk_data_pathname, "all_cdk")
    if not all_cdk_data.get("data"):
        all_cdk_data["data"] = []
    if cdk not in all_cdk_data["data"]:
        all_cdk_data["data"].append(cdk)
    else:
        await cdk_setting.finish("该CDK已存在，请更换CDK哦...", at_sender=True)
    save_data(_cdk_data_pathname, "all_cdk", all_cdk_data)

    save_data(_cdk_data_pathname, cdk, {
        "cdk": cdk,
        "money": money,
        "date": date,
        "exchanged": []
    })
    await cdk_setting.finish((
        "设置CDK成功！！\n"
        "=========\n"
        f"【CDK】{cdk}\n"
        f"【过期日期】{date}"), at_sender=True)