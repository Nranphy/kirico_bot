from kirico.utils.basic_utils import KiricoPluginMetadata


__plugin_meta__ = KiricoPluginMetadata(
    name = '雾子复读机',
    description="人类的本质是——",
    usage='''
在群友复读超过指定次数试，雾子也会参与复读哦~
当然，也可以给雾子设定终止复读√
''',
    extra={
        "author": "Nranphy",
        "version": "0.2.0",
        "repository": "",
        "visible": False,
        "default_enable": True
    }
)



# 复读
from .repeat import *

# 终止复读
from .stop import *