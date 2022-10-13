from nonebot.adapters.onebot.v11 import Event, PrivateMessageEvent, Message

from kirico.utils.basic_utils import get_config, kirico_logger
from kirico.utils.message_utils import is_text

from .repeat import message, repeat_require_least_times, message_count


repeat_stop_shortest_length = get_config("repeat_shortest_length", 1, int) 
'''对于文本消息最短打断复读长度'''
repeat_stop_require_least_times = get_config("repeat_require_least_times", 3, int) 
'''触发打断复读的重复消息条数'''

if repeat_stop_require_least_times < repeat_require_least_times:
    kirico_logger("warning", "反复读姬", "当前触发打断复读的重复消息条数（repeat_stop_require_least_times）数值小于触发复读次数（repeat_require_least_times），将会导致bot复读功能失效。")
if repeat_require_least_times <= 1:
    kirico_logger("warning", "反复读姬", "当前触发打断复读次数（repeat_stop_require_least_times）小于等于1，会导致bot对每一句话都会发送打断复读文本。")

@message.handle()
async def stop_process(event:Event):
    # 私聊信息单独判断
    if isinstance(event, PrivateMessageEvent):
        await message.finish("笨蛋~雾子才不会和你一起复读呢ww")

    group_id:int = event.group_id
    msg = event.get_message()

    cnt = message_count.get(group_id)
    if not cnt:
        await message.finish()

    if cnt >= repeat_stop_require_least_times:
        if is_text(msg) and len(msg.extract_plain_text()) < repeat_stop_shortest_length:
            await message.finish()
        else:
            message_count[group_id] = 0
            words = (
                "打断复读~！！！",
                "再次打断！！"
            )
            if is_text(msg) and msg.extract_plain_text() != words[0]:
                await message.finish(words[0])
            else:
                await message.finish(words[1])