from kirico.utils.basic_utils import KiricoPluginMetadata


__plugin_meta__ = KiricoPluginMetadata(
    name = '·雾境·',
    description="群聊中的养成RPG小游戏",
    usage='''
雾境相关指令和帮助请用【/雾境】另行查看哦
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": False,
        "default_enable": False
    }
)


# 账号相关

from .account import *



# 游戏系统
## 日常
from .daily import *
## 战斗
from .fighting import *



# 雾境查询

from .dictionary import *