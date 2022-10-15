from typing import Any, Dict, List
from nonebot import get_driver, on_command, on_notice
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent, GroupMessageEvent, GroupRecallNoticeEvent
from nonebot.rule import to_me
from nonebot.typing import T_CalledAPIHook

from .config import Config

withdraw_config = Config.parse_obj(get_driver().config.dict())


__kirico_plugin_name__ = '撤回撤回撤回'

__kirico_plugin_author__ = 'MeetWq'

__kirico_plugin_version__ = '0.1.0'

__kirico_plugin_repositorie__ = 'https://github.com/MeetWq/nonebot-plugin-withdraw'

__kirico_plugin_description__ = '诶？那是不该说的话吗...呜呜呜雾子错了...'

__kirico_plugin_usage__ = '''
想要撤回雾子的发言时，请输入【/撤回】哦~
如果要撤回倒数第x条消息，请输入【/撤回 xx】，
（ps.指令中xx是从0开始计数的！！）
当然，如果超过了限制时间...
'''

__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True


msg_ids: Dict[str, List[str]] = {}
max_size = withdraw_config.withdraw_max_size


def get_key(msg_type, id):
    return f'{msg_type}_{id}'


async def save_msg_id(bot: Bot, e: Exception, api: str, data: Dict[str, Any], result: Any) -> T_CalledAPIHook:
    try:
        if api == 'send_msg':
            msg_type = data['message_type']
            id = data['group_id'] if msg_type == 'group' else data['user_id']
        elif api == 'send_private_msg':
            msg_type = 'private'
            id = data['user_id']
        elif api == 'send_group_msg':
            msg_type = 'group'
            id = data['group_id']
        else:
            return
        key = get_key(msg_type, id)
        msg_id = result['message_id']

        if key not in msg_ids:
            msg_ids[key] = []
        msg_ids[key].append(msg_id)
        if len(msg_ids) > max_size:
            msg_ids[key].pop(0)
    except:
        pass


Bot._called_api_hook.add(save_msg_id)


withdraw = on_command('withdraw', aliases={'撤回'},
                      block=True, priority=10)


@withdraw.handle()
async def _(bot: Bot, event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        msg_type = 'group'
        id = event.group_id
    else:
        msg_type = 'private'
        id = event.user_id
    key = get_key(msg_type, id)

    if event.reply:
        msg_id = event.reply.message_id
        try:
            await bot.delete_msg(message_id=msg_id)
            return
        except:
            await withdraw.finish('撤回失败，可能已超时')

    num = event.get_plaintext().strip()
    if num and num.isdigit() and 0 <= int(num) < len(msg_ids[key]):
        num = int(num)
    else:
        num = 0

    try:
        idx = -num - 1
        await bot.delete_msg(message_id=msg_ids[key][idx])
        msg_ids[key].pop(idx)
    except:
        await withdraw.finish('撤回失败，可能已超时')


async def _group_recall(bot: Bot, event: Event) -> bool:
    if isinstance(event, GroupRecallNoticeEvent) and str(event.user_id) == str(bot.self_id):
        return True
    return False


withdraw_notice = on_notice(_group_recall, priority=10)


@withdraw_notice.handle()
async def _(event: GroupRecallNoticeEvent):
    msg_id = int(event.message_id)
    id = event.group_id
    key = get_key('group', id)
    if key in msg_ids and msg_id in msg_ids[key]:
        msg_ids[key].remove(msg_id)
