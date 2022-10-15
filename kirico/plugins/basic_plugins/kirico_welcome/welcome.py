from nonebot import on_command, on_notice, on_regex
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, GroupMessageEvent, GroupIncreaseNoticeEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.utils import DataclassEncoder

from pydantic import parse_obj_as
import json

from kirico.utils.basic_utils import kirico_logger
from kirico.utils.file_utils import get_path
from kirico.utils.message_utils import edit_img_message


_welcome_data_pathname = "welcome"



welcome_request = on_notice(priority=8)

welcome_setting = on_command("设置欢迎词", aliases={"设置欢迎信息","入群欢迎设置","欢迎词设置","群欢迎设置","设置群欢迎"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=8, block=True)

welcome_preview = on_command("查看欢迎词", aliases={"查看欢迎信息","入群欢迎查看","欢迎词查看","群欢迎查看","查看群欢迎"}, priority=8, block=True)

welcome_switch = on_regex(pattern="^/(开启|关闭)(欢迎词|群欢迎|欢迎信息)$",permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=8, block=True)



# 发送群欢迎消息
@welcome_request.handle()
async def send_welcome_msg(bot:Bot, event:GroupIncreaseNoticeEvent):
    path = get_path(_welcome_data_pathname) / f"{event.group_id}"
    
    try:
        with open(path/"setting.json", "r") as f:
            msg_information = json.load(f)
    except FileNotFoundError:
        kirico_logger("warning", "群欢迎词", "未找到入群欢迎配置，已忽略入群事件。")
        await welcome_preview.finish()
    except json.JSONDecodeError:
        kirico_logger("warning", "群欢迎词", "入群欢迎配置文件json解码失败，请检查该文件或重新设置，已忽略入群事件。")
        await welcome_preview.finish()
    except Exception as e:
        kirico_logger("warning", "群欢迎词", "获取并解析入群欢迎配置文件时出错，已忽略入群事件。")
        await welcome_preview.finish()

    msg_flag = msg_information.get("flag", False)
    msg_jsonls = msg_information.get("message",'')
    if msg_flag:
        await welcome_request.send(MessageSegment.at(event.user_id) + parse_obj_as(Message, msg_jsonls))
    else:
        kirico_logger("info", "群欢迎词", "本群未开启入群欢迎，已忽略入群欢迎。")
        await welcome_request.finish()




# 修改入群欢迎配置
@welcome_setting.handle()
async def welcome_setting_prepare(bot:Bot, event:GroupMessageEvent):
    await welcome_setting.send((
        "已进入入群欢迎信息编辑模式~\n"
        "请在下一段消息中输入所有欢迎信息√\n"
        "（ps.入群欢迎消息会自动在消息前at新人）"), at_sender = True)


@welcome_setting.got("welcome")
async def welcome_setting_process(bot:Bot, event:GroupMessageEvent, state:T_State):
    path = get_path(_welcome_data_pathname) / f"{event.group_id}"
    new_msg = await edit_img_message(state["welcome"], path)

    if new_msg:
        msg_information = {"flag":True,"message":new_msg}
        with open(path/"setting.json", "w") as f:
            json.dump(msg_information,f, cls=DataclassEncoder)
        await welcome_setting.finish((
            "欢迎词修改修改完成~可通过【/查看欢迎词】查看效果~\n"
            "已自动打开群欢迎开关√"),at_sender = True)
    else:
        await welcome_setting.finish("修改欢迎词时图片获取失败...请稍后再试哦~",at_sender = True)



# 查看群欢迎消息
@welcome_preview.handle()
async def preview_welcome_msg(bot:Bot, event:GroupMessageEvent):
    path = get_path(_welcome_data_pathname) / f"{event.group_id}"
    
    try:
        with open(path/"setting.json", "r") as f:
            msg_information = json.load(f)
    except FileNotFoundError:
        kirico_logger("warning", "群欢迎词", "未找到入群欢迎配置。")
        await welcome_preview.finish("未找到入群欢迎配置哦~\n请先通过【/设置欢迎词】设置群欢迎词~")
    except json.JSONDecodeError:
        kirico_logger("warning", "群欢迎词", "入群欢迎配置文件json解码失败，请检查该文件或重新设置。")
        await welcome_preview.finish("入群欢迎配置文件解码失败...\n请先检查文件是否有误，或通过【/设置欢迎词】设置新群欢迎词~")
    except Exception as e:
        kirico_logger("warning", "群欢迎词", "获取并解析入群欢迎配置文件时出错。")
        await welcome_preview.finish(f"获取并解析入群欢迎配置文件时失败...\n错误原因：{e}")

    msg_flag = msg_information.get("flag", False)
    msg_jsonls = msg_information.get("message",'')
    await welcome_preview.send((
        f"当前群聊入群欢迎状态为{'【开启】√' if msg_flag else '【关闭】×'}\n"
        "以下为信息内容w\n"
        "=========\n") + MessageSegment.at(event.user_id) + parse_obj_as(Message, msg_jsonls), at_sender = True
        )



# 开关群欢迎
@welcome_switch.handle()
async def welcome_switch_prepare(bot:Bot, event:GroupMessageEvent, state:T_State):
    switch_command = event.get_message().extract_plain_text()[1:3]
    if switch_command == "开启":
        state["command"] = True
    elif switch_command == "关闭":
        state["command"] = False
    else:
        await welcome_switch.finish("开关群欢迎未知错误×\n可能输入了错误指令呢...", at_sender = True)



@welcome_switch.handle()
async def welcome_switch_action(bot:Bot, event:GroupMessageEvent, state:T_State):
    path = get_path(_welcome_data_pathname) / f"{event.group_id}"

    try:
        with open(path/"setting.json", "r") as f:
            msg_information = json.load(f)
    except FileNotFoundError:
        kirico_logger("warning", "群欢迎词", "未找到入群欢迎配置。")
        await welcome_preview.finish("未找到入群欢迎配置哦~\n请先通过【/设置欢迎词】设置群欢迎词~")
    except json.JSONDecodeError:
        kirico_logger("warning", "群欢迎词", "入群欢迎配置文件json解码失败，请检查该文件或重新设置。")
        await welcome_preview.finish("入群欢迎配置文件解码失败...\n请先检查文件是否有误，或通过【/设置欢迎词】设置新群欢迎词~")
    except Exception as e:
        kirico_logger("warning", "群欢迎词", "获取并解析入群欢迎配置文件时出错。")
        await welcome_preview.finish(f"获取并解析入群欢迎配置文件时失败...\n错误原因：{e}")

    msg_flag = msg_information.get("flag", False)
    if msg_flag == state["command"]:
        await welcome_switch.finish(f"本群入群欢迎状态早已是{'【开启】' if msg_flag else '【关闭】'}了哦~", at_sender = True)
    else:
        msg_information["flag"] = state["command"]
        try:
            with open(path/"setting.json", "w") as f:
                json.dump(msg_information,f)
        except Exception as e:
            await welcome_switch.finish(f"设置入群欢迎信息开关时发生错误×\n错误原因：{e}", at_sender = True)
        await welcome_switch.finish(f"设置成功~\n本群入群欢迎信息状态为【{'开启' if state['command'] else '关闭'}】", at_sender = True)