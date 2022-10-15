from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Message

from kirico.utils.basic_utils import get_plugin_metadata, if_plugin_exists


info_request = on_command("info",aliases={"插件信息","插件详细"}, priority=5, block=True)

@info_request.handle()
async def info_request_info(arg:Message = CommandArg()):
    name = arg.extract_plain_text().strip()
    if not if_plugin_exists(name):
        await info_request.finish(f"你所查询的插件【{name}】不存在...", at_sender=True)
    metadata = get_plugin_metadata(name)
    if not metadata:
        await info_request.finish(f"你所查询的插件【{name}】不存在Metadata哦...", at_sender=True)
    await info_request.finish(
        (
            f"【{name}】插件信息\n"
            "=========\n"+
            (f"插件作者：{metadata.author}\n" if hasattr(metadata, "author") and metadata.author else "未知\n")+
            (f"插件版本：{metadata.version}\n" if hasattr(metadata, "version") and metadata.version else "未知\n")+
            (f"插件仓库：{metadata.repository}\n" if hasattr(metadata, "repository") and metadata.repository else "未知\n")+
            "=========\n"
            "感谢插件作者的开源奉献哦~"
            )
            ,at_sender = True
    )