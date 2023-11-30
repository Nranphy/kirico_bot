from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent, GROUP_ADMIN, GROUP_OWNER

from .utils import control_groupchat_switch, control_plugin_switch, if_plugin_exists



plugin_switch_off = on_command("关闭插件",aliases={"插件关闭","禁用插件","插件禁用"},priority=1,block=True,permission=SUPERUSER|GROUP_OWNER|GROUP_ADMIN)

plugin_switch_on = on_command("开启插件",aliases={"插件开启","启用插件","插件启用"},priority=1,block=True,permission=SUPERUSER|GROUP_OWNER|GROUP_ADMIN)

groupchat_switch_off = on_command("bot off",aliases={"闭嘴","机器人关闭","关闭机器人","关闭群聊","关闭"},priority=1,block=True,permission=SUPERUSER|GROUP_OWNER|GROUP_ADMIN)

groupchat_switch_on = on_command("bot on",aliases={"说话","机器人开启","开启机器人","开启群聊","开启"},priority=1,block=True,permission=SUPERUSER|GROUP_OWNER|GROUP_ADMIN)





@plugin_switch_off.handle()
async def plugin_switch_off_process(bot:Bot, event:GroupMessageEvent, arg:Message = CommandArg()):
    name = arg.extract_plain_text().strip()
    if not name:
        await plugin_switch_off.finish("未指定插件名称...请再检查哦。", at_sender=True)
    
    if name==__package__.split('.')[-1]:
        await plugin_switch_off.finish("不能开关本管理插件哦~\n如果不想要雾子说话的话，请使用指令【/关闭】√", at_sender=True)
    
    if not if_plugin_exists(name):
        await plugin_switch_off.finish(
            ("指定插件名不在插件名单中，雾子只接受英文插件名哦...\n"
            "请检查插件名拼写（如大小写和下划线），或使用【/help】进行插件菜单查询。"), at_sender=True)
    
    control_plugin_switch_result = control_plugin_switch(name, False, event.group_id)
    if control_plugin_switch_result[0]:
        await plugin_switch_off.finish(f"插件 {name} 在本群禁用成功~", at_sender=True)
    else:
        if control_plugin_switch_result[1] == 202:
            await plugin_switch_off.finish(f"插件 {name} 在本群已经是禁用了的哦~", at_sender=True)


@plugin_switch_on.handle()
async def plugin_switch_on_process(bot:Bot, event:GroupMessageEvent, arg:Message = CommandArg()):
    name = arg.extract_plain_text().strip()
    if not name:
        await plugin_switch_off.finish("未指定插件名称...请再检查哦。", at_sender=True)
    
    if name==__package__.split('.')[-1]:
        await plugin_switch_off.finish("不能开关本管理插件哦~\n如果不想要雾子说话的话，请使用指令【/关闭】√", at_sender=True)
    
    if not if_plugin_exists(name):
        await plugin_switch_off.finish(
            ("指定插件名不在插件名单中，雾子只接受英文插件名哦...\n"
            "请检查插件名拼写（如大小写和下划线），或使用【/help】进行插件菜单查询。"), at_sender=True)
    
    control_plugin_switch_result = control_plugin_switch(name, True, event.group_id)
    if control_plugin_switch_result[0]:
        await plugin_switch_off.finish(f"插件 {name} 在本群启用成功~", at_sender=True)
    else:
        if control_plugin_switch_result[1] == 202:
            await plugin_switch_off.finish(f"插件 {name} 在本群已经是启用了的哦~", at_sender=True)


@groupchat_switch_off.handle()
async def groupchat_switch_off_process(bot:Bot, event:GroupMessageEvent):
    control_groupchat_switch_result = control_groupchat_switch(False, event.group_id)
    if control_groupchat_switch_result[0]:
        await groupchat_switch_off.finish("呜呜...雾子闭嘴啦...", at_sender=True)
    else:
        if control_groupchat_switch_result[1] == 202:
            await groupchat_switch_off.finish("雾子已经是关闭状态啦...（小声）", at_sender=True)


@groupchat_switch_on.handle()
async def groupchat_switch_on_process(bot:Bot, event:GroupMessageEvent):
    control_groupchat_switch_result = control_groupchat_switch(True, event.group_id)
    if control_groupchat_switch_result[0]:
        await groupchat_switch_off.finish(f"雾子回来了哦~", at_sender=True)
    else:
        if control_groupchat_switch_result[1] == 202:
            await groupchat_switch_off.finish(f"雾子已经可以说话了啦！！！", at_sender=True)