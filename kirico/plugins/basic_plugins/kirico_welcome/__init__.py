from kirico.utils.basic_utils import KiricoPluginMetadata


__plugin_meta__ = KiricoPluginMetadata(
    name = '入群欢迎喵~！！',
    description="让雾子来欢迎新人吧~",
    usage='''
【/设置欢迎词】 群主与群管可设置雾子的入群欢迎信息（支持at现有群员、文本、图片），同时开启雾子入群欢迎
【/查看欢迎词】 群员均可查看入群欢迎开关状态和欢迎内容
【/开启欢迎词 | /关闭欢迎词】 群主与群管可开关雾子入群欢迎功能
若需清除现有欢迎词，请使用设置功能进行覆盖哦~
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": True,
        "default_enable": True
    }
)

# 欢迎相关
from .welcome import *