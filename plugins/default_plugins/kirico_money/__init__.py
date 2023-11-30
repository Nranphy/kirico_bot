from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name = '雾团子货币~',
    description="雾团子...好次！！",
    usage='''
签到、互动可以获得雾团子√
雾团子是像货币一样的东西、可在支持雾团子的各个系统使用~
雾团子查询【/查询雾团子】
CDK可用【/cdk xxxx】进行兑换
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": True,
        "default_enable": True
    }
)


# 雾团子相关
from .money import *

# CDK相关
from .cdk import *