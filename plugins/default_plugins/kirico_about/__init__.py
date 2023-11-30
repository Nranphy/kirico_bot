from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name = '关于与反馈',
    description="要查看雾子的信息吗~",
    usage='''
使用【/关于】查看雾子关于信息√
对雾子的反馈和建议请使用【/反馈 xxx】，雾子会好好转达给作者桑的哦~
(ps.其中xxx为消息和图片，请在同一消息中发送。如有多段文本，可多次使用该指令哦~)
''',
    homepage = None,
    config = None,
    extra={
        "author": "Nranphy",
        "visible": True,
        "default_enable": True
    }
)



# 关于
from .about import *

# 反馈
from .feedback import *