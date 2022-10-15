from kirico.utils.basic_utils import KiricoPluginMetadata


__plugin_meta__ = KiricoPluginMetadata(
    name = '能不能好好说话！！',
    description="u1s1用缩写真是duck不必（指指点点）",
    usage='''
发送【/缩写 xxx】来查找该缩写的可能解释~
米娜要好好说话哦×
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": True,
        "default_enable": True
    }
)



# 获取缩写
from .get_data import *