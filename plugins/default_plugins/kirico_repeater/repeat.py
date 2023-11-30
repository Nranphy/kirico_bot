from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent, PrivateMessageEvent, Message

from utils.basic_utils import get_config, kirico_logger
from utils.message_utils import is_text, message_equal



repeat_shortest_length = get_config("repeat_shortest_length", 1, int) 
'''对于文本消息最短复读长度'''
repeat_require_least_times = get_config("repeat_require_least_times", 3, int) 
'''触发复读的重复消息条数'''
repeat_max_times = get_config("repeat_max_times", 1, int)
'''bot进行复读的最多次数'''

if repeat_require_least_times <= 1:
    kirico_logger("warning", "复读姬", "当前触发复读次数（repeat_require_least_times）小于等于1，会导致bot复读每一句话，或将导致风控。")

message_temp:dict[str,Message] = {}
'''各群消息临时存放'''
message_count:dict[str,int] = {}
'''其他成员进行复读的次数'''
repeat_count:dict[str,int] = {}
'''bot在某群的发送复读次数'''


message = on_message(priority=99, block=False)


@message.handle()
async def repeater_process(event:MessageEvent):
    # 单独处理私聊消息
    if isinstance(event, PrivateMessageEvent):
        await message.finish()
    
    group_id:str = str(event.group_id)
    
    new_message = event.get_message()

    old_message = message_temp.get(group_id)
    if old_message and message_equal(new_message, old_message):
        message_count[group_id] += 1
    else:
        message_temp[group_id] = new_message
        message_count[group_id] = 1
        repeat_count[group_id] = 0

    if message_count[group_id] >= repeat_require_least_times and \
        repeat_count[group_id] < repeat_max_times:
            # 对文本信息单独判断
            if is_text(new_message) and len(new_message.extract_plain_text()) < repeat_shortest_length:
                pass
            else:
                await message.send(new_message)
                repeat_count[group_id] += 1
                message_count[group_id] = 0 # 重置后，bot会在等再次达到目标重复消息数时再次复读