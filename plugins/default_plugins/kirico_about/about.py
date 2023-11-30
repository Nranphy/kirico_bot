from nonebot import on_regex, on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher


async def about_send(matcher: Matcher):
    msg = (
        "这里是雾子酱~\n"
        "插件功能帮助请输入【/help】\n"
        "对雾子的反馈和建议请使用【/反馈 xxx】\n"
        "作者QQ：3102002900\n"
        "开源仓库：https://github.com/nranphy/kirico_bot/"
    )
    await matcher.send(msg)


about_request_regex = on_regex("^关于$", priority=5, block=True, rule=to_me(),handlers=[about_send])

about_request_command = on_command("关于",aliases={"about"}, priority=6, block=True, handlers=[about_send])