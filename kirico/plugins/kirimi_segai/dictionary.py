from nonebot import on_command, get_bot, get_driver, on_startswith
from nonebot.typing import T_State
from nonebot.params import State, CommandArg
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent
from nonebot.log import logger
from kirico.utils.file_utils import check_dir, check_file, rm_path
from kirico.utils.message_utils import send_forward_msg
import time
import os
import json
import random
import re


# 查询接口

kirico_segai_help = on_command("雾境",priority=9,block=True)

#查询处理

@kirico_segai_help.handle()
async def help_handle(bot:Bot, event:Event, arg:Message=CommandArg()):
    command = arg.extract_plain_text().strip().split()
    if not command or "help" in command or "帮助" in command or "菜单" in command:
        await kirico_segai_help.finish(
            '''【雾境指令菜单】
===账号===
【/注册】获取注册表单和注册详情
【/查看账号】获得账号详细信息
【/删除账号】根据提示删除个人账号
===游戏===
【/购买经验 xxx】用雾团子购买经验，xxx为数量
【/加点 XXX xxx】向XXX素质加点xxx点，具体请通过[/加点]了解
【/更换装备 xxx】更换上已有装备，xxx为装备序号，可通过[/查看账号]了解
【/脱下装备】取下所有身上装备
【/添加技能 xxx】添加上已有技能，xxx为技能英文名，可以有多个技能名，用空格分隔。技能名可通过[/查看账号]了解
【/清除技能 xxx】取下已装备的技能，xxx为技能英文名，可以有多个技能名，用空格分隔
【/清空技能】换下所有已添加技能，而非丢弃技能
【/决斗 xxx】向指定玩家进行决斗，xxx可为at或者QQ号
【/转职 xxx】可以进行转职。查看当前可转职业请用[/购买经验 1]
===查询===
敬请期待。
目前可用【/雾境】查看菜单''',at_sender=True)
    # 读取多个json字典文件
    dic = dict()
    dic_path = os.path.abspath(os.path.dirname(__file__))+"/resources/dictionary/"
    file_ls = os.listdir(dic_path)
    try:
        for file in file_ls:
            with open(os.path.join(dic_path,file),"r",encoding="UTF-8-sig") as f:
                dic.update(json.load(f))
    except:
        await kirico_segai_help.finish("字典文件查询出错×",at_sender=True)
    msgs = ["你的查询结果如下哦~\nps.可用空格分隔多个词条，雾子将分别查询每一个词条哦~"]
    for i in command:
        msg = dic.get(i,f"未找到词条【{i}】的相关信息...")
        msgs.append(f"词条【{i}】的注释为\n=========\n"+msg)
    msgs.append("=========\n查询结束~")
    await kirico_segai_help.send("查询词条成功~\n具体内容请查看合并消息~",at_sender=True)
    await send_forward_msg(bot,event,"「雾境」",bot.self_id,msgs)
    await kirico_segai_help.finish()


# 更改查询种族、装备等接口