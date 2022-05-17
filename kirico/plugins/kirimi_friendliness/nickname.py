from nonebot import on_command, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, GroupMessageEvent
from nonebot.log import logger
from kirico.utils.friendliness_utils import friendliness_inquire
from kirico.utils.file_utils import check_dir, check_file
import os
import json






nickname_setting_request = on_command("nickname", aliases={"设置别名","叫我","设置称呼","设置昵称","设定称呼","设定昵称","设定别名"}, priority=7, block=True)


@nickname_setting_request.handle()
async def nickname_setting_prepare(bot:Bot, event:Event, arg:Message=CommandArg(), state:T_State = State()):
    arg = arg.extract_plain_text().split()
    if arg:
        state["nickname"] == arg

@nickname_setting_request.got("nickname",prompt="想要雾子怎样称呼你呢~")
async def nickname_setting(bot:Bot, event:Event, state:T_State = State()):
    qq = event.get_user_id()
    json_path = os.getcwd()+f"/kirico/data/nickname.json"
    check_dir(os.getcwd()+f"/kirico/data/")
    check_file(json_path)

    if friendliness_inquire(qq)[0] < 200:
        await nickname_setting_request.finish("抱歉...\n先和雾子从朋友做起好吗？（微笑）", at_sender=True)

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except:
            data = dict()
    
    data[qq] = str(state["nickname"])

    try:
        with open(json_path, "w+") as f:
            json.dump(data,f)
    except:
        await nickname_setting_request.finish("数据读写失败...请不要用文本以外的信息哦×\n要再试一次吗?", at_sender=True)

    await nickname_setting_request.finish(f"设置成功~\n雾子以后就叫你 {str(state['nickname'])} 了哦√", at_sender=True)


special_title_setting_request = on_command("设置头衔", aliases={"头衔设置","头衔","专属头衔"}, priority=7, block=True)

@special_title_setting_request.handle()
async def special_title_setting_prepare(bot:Bot, event:GroupMessageEvent, arg:Message=CommandArg(), state:T_State = State()):
    arg = arg.extract_plain_text().split()
    if arg:
        state["title"] == arg

@special_title_setting_request.got("title")
async def special_title_setting(bot:Bot, event:GroupMessageEvent, state:T_State = State()):
    qq = event.get_user_id()
    if friendliness_inquire(qq)[0] < 100:
        await special_title_setting_request.finish("雾子...和你不是很熟呢×\n可以多和雾子相处吗？", at_sender=True)

    try:
        await bot.set_group_special_title(group_id=event.group_id,user_id=qq,special_title=state["title"])
        await special_title_setting_request.finish("设置成功哦~", at_sender=True)
    except:
        await special_title_setting_request.finish("设置失败呢...\n请检查头衔是否在六个字以内并没有特殊字符哦~", at_sender=True)