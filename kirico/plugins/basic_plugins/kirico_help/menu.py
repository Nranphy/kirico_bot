from nonebot import on_command
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.plugin import get_loaded_plugins, Plugin
from nonebot.adapters.onebot.v11 import Bot, Event


help_request = on_command("help",aliases={"帮助","菜单","功能"}, priority=5, block=True)



@help_request.handle()
async def do_something_first(bot: Bot, event: Event, state: T_State = State()):
    plugins_list = [plugin for plugin in sorted(list(get_loaded_plugins()), key=lambda x:x.name) if plugin.metadata and hasattr(plugin.metadata, "visible") and plugin.metadata.visible]
    state["plugins"] = plugins_list

    plugins_menu_ls = [f"{index+1}." + plugins_list[index].name + ' | ' + plugins_list[index].metadata.name for index in range(len(plugins_list))]

    await help_request.send((
        "有人在呼唤雾子酱吗ww\n"
        "锵锵~这里是雾子酱已加载插件菜单√\n"
        "=========\n"+
        ('\n'.join(plugins_menu_ls))+"\n"
        "=========\n"
        "如需查看某一插件的用法，请直接回复对应数字哦~"
    ), at_sender=True)
    
        


@help_request.got("target")
async def get_plugin_help(bot: Bot, event: Event, state: T_State = State()):
    # 对用户给予字符串进行处理并判断
    target:str = state["target"].extract_plain_text()
    if target.isdigit():
        # 数字不在给予的范围内则重新选择
        target:int = int(target) - 1
        if not (0<=target<len(state["plugins"])):
            await help_request.reject("数字不在范围内哦...请重新输入查询√")
    else:
        await help_request.finish("检测到非数字，雾子菜单查询结束√", at_sender=True)
    
    plugin:Plugin = state["plugins"][target]

    plugin_name = plugin.metadata.name.strip()
    plugin_description = plugin.metadata.description.strip()
    plugin_usage = plugin.metadata.usage.strip()

    await help_request.reject(
        ("查询插件帮助成功~\n"
        "=========\n"
        f"【{plugin.name}】{plugin_name}\n"
        f"{plugin_description}\n"
        "=========\n"
        f"{plugin_usage}\n"
        "=========\n"
        "若需查询其他插件，请再次输入数字哦~\n"
        "使用【/插件详细 (插件名)】查看作者等信息哦~"), at_sender=True)