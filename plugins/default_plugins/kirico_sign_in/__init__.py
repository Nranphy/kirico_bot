from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name = '雾子签到',
    description="雾子只想知道是否仍被在意呢...",
    usage='''
每天可以发送指令【/签到】向雾子酱签到~可获得雾团子和好感度×
每天只能签到一次——嗯？不正常吗？
想查看签到状态的话可以用【/签到查询】哦~
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": True,
        "default_enable": True
    }
)

# 签到相关
from .sign_in import *

# 查询签到
from .query import *