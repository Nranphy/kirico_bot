from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name = '雾子酱控制器',
    description="雾子...读取完毕——",
    usage='''
控制雾子酱在群聊时的表现√
===
需要在不同群开关插件吗？用【/help】获得插件英文名再使用以下命令控制√
【/关闭插件 xxx】xxx为获取的插件英文名
【/开启插件 xxx】xxx为获取的插件英文名
插件默认均为开启哦~ 另外本管理插件不能禁用√
===
本群有风险或者暂时不需要雾子，可以暂时关闭雾子哦
【/关闭】关闭雾子所有其他功能，只留下本插件
【/开启】恢复雾子所有功能，但不会重置插件开关哦
===
不需要雾子了吗...？请使用安全的退群方式哦...
【/退群】可按提示让雾子安全的退群
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": True,
        "default_enable": True
    }
)



# 指令开关插件
from .switch import *

# 退群指令
from .dismiss import *

# 各种钩子函数
from .hooks import *