from kirico.utils.basic_utils import KiricoPluginMetadata


__plugin_meta__ = KiricoPluginMetadata(
    name = '雾子好感度♡',
    description="雾子...dokidoki♡",
    usage='''
和雾子酱互动、使用各种功能可以增加雾子酱的好感度哦~
===
好感度查询吧~【/查询好感度】
诶？想让雾子更换称呼？好感度超过200可使用【/设置称呼 xxx】来设定爱称√
雾子是群主的话可以用【/设置头衔 xxx】来获取头衔哦~
===
通过每天不同时间的问候来增加雾子的好感度吧~
注意问候语要带上雾子关键词哦√
请不要一直重复问候雾子哦，雾子也是会厌烦的！！
不过，如果问候的时间错误的话...
另外，好感度超过一定值时雾子也会主动问好哦~
===
好感度到达一定程度可以和雾子交互哦...
请自行探索交互选项吧~
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": True,
        "default_enable": True
    }
)

# 查询好感
from .query import *

# 更改称呼或者群头衔
from .designation import *

# 交互行为
from .interactivity import *
# 戳一戳
from .pokepoke import *

# 问候与自动问候
from .greetings import *