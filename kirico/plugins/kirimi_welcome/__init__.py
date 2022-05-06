from nonebot import on_command, get_bot, get_driver, on_notice, on_regex
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent, GroupIncreaseNoticeEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.log import logger
from nonebot.utils import DataclassEncoder
from pydantic import parse_obj_as
from kirico.utils.file_utils import check_dir, check_file
from kirico.utils.message_utils import edit_img_message
import os
import json




__kirico_plugin_name__ = '雾子酱的入群欢迎'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.0.7'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '让雾子来欢迎新人吧~'

__kirico_plugin_usage__ = '''
【/设置欢迎词】 群主与群管可设置雾子的入群欢迎信息（支持at现有群员、文本、图片），同时开启雾子入群欢迎
【/查看欢迎词】 群员均可查看入群欢迎开关状态和欢迎内容
【/开启欢迎词 | /关闭欢迎词】 群主与群管可开关雾子入群欢迎功能
若需清除现有欢迎词，请使用设置功能进行覆盖哦~
'''

__kirico__plugin_visible__ = True






welcome_request = on_notice(priority=8)

welcome_setting = on_command("设置欢迎词", aliases={"设置欢迎信息","入群欢迎设置","欢迎词设置","群欢迎设置","设置群欢迎"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=8, block=True)

welcome_preview = on_command("查看欢迎词", aliases={"查看欢迎信息","入群欢迎查看","欢迎词查看","群欢迎查看","查看群欢迎"}, priority=8, block=True)

welcome_switch = on_regex(pattern="^/(开启|关闭)(欢迎词|群欢迎|欢迎信息)$",permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=8, block=True)



# 发送群欢迎消息
@welcome_request.handle()
async def send_welcome_msg(bot:Bot, event:GroupIncreaseNoticeEvent):
    msg_path = os.getcwd()+f"/kirico/data/welcome/{event.group_id}/welcome_text.json"
    check_dir(os.getcwd()+f"/kirico/data/welcome/{event.group_id}/")
    check_file(msg_path)
    try:
        with open(msg_path,"r") as f:
            msg_information = json.load(f)
    except FileNotFoundError:
        logger.warning("未找到入群欢迎配置，已忽略入群欢迎。")
        await welcome_request.finish()
    except json.JSONDecodeError:
        logger.warning("入群欢迎配置文件json解码失败，请检查该文件或重新设置。已忽略入群欢迎。")
        await welcome_request.finish()
    except Exception as e:
        logger.warning("获取并解析入群欢迎配置文件时出错，已忽略入群欢迎。")

    msg_flag = msg_information.get("flag", False)
    msg_jsonls = msg_information.get("message",'')
    if msg_flag:
        await welcome_request.send(MessageSegment.at(event.user_id)+parse_obj_as(Message, msg_jsonls))
    else:
        logger.info("本群未开启入群欢迎，已忽略入群欢迎。")
        await welcome_request.finish()




# 修改入群欢迎配置
@welcome_setting.handle()
async def welcome_setting_prepare(bot:Bot, event:GroupMessageEvent, state:T_State = State()):
    await welcome_setting.send("已进入入群欢迎信息编辑模式~\n请在下一段消息中输入所有欢迎信息√\n（ps.入群欢迎消息会自动在消息前at新人）")


@welcome_setting.got("welcome")
async def welcome_setting_process(bot:Bot, event:GroupMessageEvent, state:T_State = State()):
    msg_path = os.getcwd()+f"/kirico/data/welcome/{event.group_id}/welcome_text.json"
    path = os.getcwd()+f"/kirico/data/welcome/{event.group_id}/"
    check_dir(path)
    check_file(msg_path)
    new_msg = await edit_img_message(state["welcome"], path)
    if new_msg:
        msg_information = {"flag":True,"message":new_msg}
        with open(msg_path,"w+") as f:
            json.dump(msg_information,f, cls=DataclassEncoder)
        await welcome_setting.finish("公告修改修改完成~可通过【/查看欢迎词】查看效果~\n已自动打开群欢迎开关√",at_sender = True)
    else:
        await welcome_setting.finish("修改公告时图片获取失败...请稍后再试哦~",at_sender = True)



# 查看群欢迎消息
@welcome_preview.handle()
async def preview_welcome_msg(bot:Bot, event:GroupMessageEvent):
    msg_path = os.getcwd()+f"/kirico/data/welcome/{event.group_id}/welcome_text.json"
    check_dir(os.getcwd()+f"/kirico/data/welcome/{event.group_id}/")
    check_file(msg_path)
    try:
        with open(msg_path,"r") as f:
            msg_information = json.load(f)
    except FileNotFoundError:
        logger.warning("未找到入群欢迎配置。")
        await welcome_preview.finish("未找到入群欢迎配置哦~\n请先通过 “/设置欢迎词” 设置群欢迎词~")
    except json.JSONDecodeError:
        logger.warning("入群欢迎配置文件json解码失败，请检查该文件或重新设置。")
        await welcome_preview.finish("入群欢迎配置文件解码失败...\n请先检查文件是否有误，或通过【/设置欢迎词】设置新群欢迎词~×")
    except Exception as e:
        logger.warning("获取并解析入群欢迎配置文件时出错。")
        await welcome_preview.finish(f"获取并解析入群欢迎配置文件时失败...\n错误原因：{e}")

    msg_flag = msg_information.get("flag", False)
    msg_jsonls = msg_information.get("message",'')
    if msg_flag:
        await welcome_preview.send("当前群聊入群欢迎状态为【开启】√\n以下为信息内容w\n=========\n"+MessageSegment.at(event.user_id)+parse_obj_as(Message, msg_jsonls))
    elif msg_jsonls:
        await welcome_preview.send("当前群聊入群欢迎状态为【关闭】×\n以下为信息内容w\n=========\n"+MessageSegment.at(event.user_id)+parse_obj_as(Message, msg_jsonls))
    else:
        logger.info("本群并未设置欢迎词。")
        await welcome_preview.finish("当前群聊并未开启入群欢迎哦...\n请输入【/设置欢迎词】来设置入群欢迎吧~",at_sender = True)



# 开关群欢迎
@welcome_switch.handle()
async def welcome_switch_prepare(bot:Bot, event:GroupMessageEvent, state:T_State = State()):
    switch_command = str(event.get_message())[1:3]
    if switch_command == "开启":
        state["command"] = True
    elif switch_command == "关闭":
        state["command"] = False
    else:
        await welcome_switch.finish("开关群欢迎未知错误×\n可能输入了错误指令呢...",at_sender = True)



@welcome_switch.handle()
async def welcome_switch_action(bot:Bot, event:GroupMessageEvent, state:T_State = State()):
    msg_path = os.getcwd()+f"/kirico/data/welcome/{event.group_id}/welcome_text.json"
    check_dir(os.getcwd()+f"/kirico/data/welcome/{event.group_id}/")
    check_file(msg_path)
    try:
        with open(msg_path,"r") as f:
            msg_information = json.load(f)
    except FileNotFoundError:
        logger.warning("未找到入群欢迎配置。")
        await welcome_switch.finish("未找到入群欢迎配置哦~\n请先通过【/设置欢迎词】设置群欢迎词~")
    except json.JSONDecodeError:
        logger.warning("入群欢迎配置文件json解码失败，请检查该文件或重新设置。")
        await welcome_switch.finish("入群欢迎配置文件解码失败...\n请先检查文件是否有误，或通过【/设置欢迎词】设置新群欢迎词~×")
    except Exception as e:
        logger.warning("获取并解析入群欢迎配置文件时出错。")
        await welcome_switch.finish(f"获取并解析入群欢迎配置文件时失败...\n错误原因：{e}")

    msg_flag = msg_information.get("flag", False)
    msg_jsonls = msg_information.get("message",'')
    if not msg_jsonls:
        await welcome_switch.finish("未找到入群欢迎配置哦~\n请先通过【/设置欢迎词】设置群欢迎词~",at_sender = True)
    elif msg_flag == state["command"] == True:
        await welcome_switch.finish("本群入群欢迎状态早已是【开启】了哦~",at_sender = True)
    elif msg_flag == state["command"] == False:
        await welcome_switch.finish("本群入群欢迎状态已经是【关闭】了哦~",at_sender = True)
    else:
        msg_information["flag"] = state["command"]
        try:
            with open(msg_path,"w+") as f:
                json.dump(msg_information,f)
        except Exception as e:
            await welcome_switch.finish(f"设置入群欢迎信息开关时发生错误×\n错误原因：{e}",at_sender = True)
        switch_statu_inzh = "开启" if state["command"] else "关闭"
        await welcome_switch.finish(f"设置成功~\n本群入群欢迎信息状态为【{switch_statu_inzh}】",at_sender = True)


    






# async def edit_img_message(msg:Message, event:Event) -> Message:
#     '''
#     对传入Message进行处理，下载图片并替换图片data地址。
#     :param msg: 传入的消息段
#     :返回新Message（其实已经对原Message做出了更改），失败则返回False.
#     '''
#     new_msg = Message()
#     for seg in msg:
#         if seg.type == "image":
#             url = seg.data.get("url", "")
#             filename = seg.data.get("file", "")
#             if filename and url:
#                 img = await get_img(url)
#                 path = os.getcwd()+f"/kirico/data/welcome/{event.group_id}/{filename}"
#                 if img:
#                     await save_img(img, path)
#                     seg.data["file"] = f"file:///"+path
#                 else:
#                     return False
#         new_msg.append(seg)
#     return new_msg



# # 已找到好的方法来持久化Message实例，使用DataclassEncoder
# def serialize_message(msg: Message) -> str:
#     '''
#     将Message实例转化成json化字符串
#     :感谢meetwq佬！！
#     '''
#     return json.dumps(
#         [{"type": seg.type, "data": seg.data} for seg in msg],
#         ensure_ascii=False
#     )

# def deserialize_message(msg: str) -> Message:
#     '''
#     将传入json化字符串转化成Message实例
#     :感谢meetwq佬！！
#     '''
#     return parse_obj_as(Message, json.loads(msg))