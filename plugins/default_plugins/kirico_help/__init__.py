from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name = '雾子插件帮助菜单',
    description="雾子酱的料理菜单~",
    usage='''
发送指令【/help】或【/帮助】获取已加载插件菜单，
输入返回的插件序号进行插件帮助查询。
通过指令【/info xxx】或【/插件信息 xxx】获得插件仓库、作者等信息，xxx为插件英文名√
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": True,
        "default_enable": True
    }
)



# 帮助菜单
from .menu import *

# 插件详情
from .info import *