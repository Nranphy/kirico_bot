import nonebot

print(
      "| \033[0;36m _  ___      _           ____        _   \033[0m |\n"
      "| \033[0;36m| |/ (_)    (_)         |  _ \\      | |  \033[0m |\n"
      "| \033[0;36m| ' / _ _ __ _  ___ ___ | |_) | ___ | |_ \033[0m |\n"
      "| \033[0;36m|  < | | '__| |/ __/ _ \\|  _ < / _ \\| __|\033[0m |\n"
      "| \033[0;36m| . \\| | |  | | (_| (_) | |_) | (_) | |_ \033[0m |\n"
      "| \033[0;36m|_|\\_\\_|_|  |_|\\___\\___/|____/ \\___/ \\__|\033[0m |\n"
      )

# 设置日志输出
from nonebot.log import logger, default_format
logger.add("logs/error.log",
           rotation="00:00",
           diagnose=False,
           level="ERROR",
           format=default_format)

# NoneBot 初始化
nonebot.init()
app = nonebot.get_asgi()

# 注册适配器
driver = nonebot.get_driver()

# 载入插件
# 多平台适配插件
nonebot.load_plugin("plugins.special_plugins.kirico_plugin_sekaiju")
# 先行载入部分关键插件，避免异常
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin("nonebot_plugin_htmlrender")
# 导入其余插件
nonebot.load_from_toml("pyproject.toml")



if __name__ == "__main__":
    nonebot.run(
        app="__mp_main__:app"
        )