from nonebot import on_command, require, get_bot, get_driver
from nonebot.typing import T_State
from nonebot.params import State, CommandArg, Arg
from nonebot.plugin.plugin import get_loaded_plugins, get_plugin
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.log import logger
import os



__kirico_plugin_name__ = '雾子酱帮助菜单'

__kirico_plugin_author__ = 'Nranphy'

__kirico_plugin_version__ = '0.0.5'

__kirico_plugin_repositorie__ = ''

__kirico_plugin_description__ = '雾子酱专用的插件帮助菜单~'

__kirico_plugin_usage__ = '''
发送指令/help获取已加载插件菜单，
输入返回的插件序号进行插件帮助查询。
'''

__kirico__plugin_visible__ = True




help_request = on_command("help",aliases={"帮助","菜单","功能"}, priority=5, block=True)




@help_request.handle()
async def do_something_first(bot: Bot, event: Event, state: T_State = State()):
    plugins_list_origin = sorted(list(get_loaded_plugins()), key=lambda x:x.name) # 处理后不会再用到
    plugins_list = list()
    # 检测插件内设置菜单是否可见，默认为不可见
    for plugin in plugins_list_origin:
        try:
            plugin_visible = plugin.module.__getattribute__("__kirico__plugin_visible__")
        except:
            plugin_visible = False
        if plugin_visible:
            plugins_list.append(plugin)
    state["plugins"] = plugins_list

    plugins_name_ls = list()
    for plugin in plugins_list:
        try:
            plugins_name_ls.append(plugin.module.__getattribute__("__kirico_plugin_name__").strip() + ' | ' +plugin.name)
        except Exception:
            plugins_name_ls.append(plugin.name)

    msg = ' 有人在呼唤雾子酱吗ww\n锵锵~这里是雾子酱已加载插件菜单√\n=========\n'
    for i in range(len(plugins_name_ls)):
        msg += f'{i+1}. ' + plugins_name_ls[i] + '\n'
    msg += '=========\n如需查看某一插件的用法，请直接回复对应数字哦~'

    await help_request.send(msg, at_sender=True)
    
        


@help_request.got("target")
async def get_plugin_help(bot: Bot, event: Event, state: T_State = State()):
    # 对用户给予字符串进行处理并判断
    state["target"] = str(state["target"])
    if state["target"].isdigit():
        state["target"] = int(state["target"]) - 1 if 0<int(state["target"])<=len(state["plugins"]) else len(state["plugins"]) # 如果数字不在给予的范围内，给他一个越界的索引值，触发下文的IndexError
    else:
        await help_request.finish("检测到非数字，雾子菜单查询结束√", at_sender=True)
    # 尝试获取插件信息并考虑全部情况
    try:
        plugin_description = state["plugins"][state["target"]].module.__getattribute__("__kirico_plugin_description__").strip() +'\n'
    except Exception:
        plugin_description = ''
    try:
        plugin_usage = state["plugins"][state["target"]].module.__getattribute__("__kirico_plugin_usage__").strip()
    except IndexError:
        await help_request.reject("输入数字不在范围内！！请再次输入×", at_sender=True)
    except TypeError:
        await help_request.finish("该插件的帮助属性有误呜呜呜...\n已结束查询×", at_sender=True)
    except AttributeError:
        await help_request.finish("该插件还没有帮助文本呢...\n已结束查询×", at_sender=True)
    except Exception as e:
        await help_request.finish(f"查询帮助时发生未知错误...错误类型 {e}\n已结束查询×", at_sender=True)
    
    await help_request.reject(f'查询插件帮助成功~\n=========\n【{state["plugins"][state["target"]].name}】\n{plugin_description}=========\n{plugin_usage}\n=========\n若需查询其他插件，请再次输入数字哦~', at_sender=True)


# 查询某插件信息指令（作者等等）