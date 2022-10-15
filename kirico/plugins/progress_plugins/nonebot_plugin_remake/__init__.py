import re
import random
import asyncio
import itertools
import traceback
from typing import List, Tuple, Optional
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.params import ArgPlainText, State
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
)
from nonebot.log import logger

from .life import Life
from .talent import Talent

__kirico_plugin_name__ = 'Remake:人生重来！！'

__kirico_plugin_author__ = 'MeetWq'

__kirico_plugin_version__ = '0.1.0'

__kirico_plugin_repositorie__ = 'https://github.com/MeetWq/nonebot-plugin-remake'

__kirico_plugin_description__ = '这垃圾人生一秒也不想待了？立即重开！'

__kirico_plugin_usage__ = '''
输入【/remake | /人生重来 | /人生重开】进行转生√
可是...转生后真的比现在快乐吗...
'''

__kirico_plugin_visible__ = True

__kirico_plugin_default__ = True


remake = on_command(
    "remake",
    aliases={"liferestart", "人生重开", "人生重来"},
    block=True,
    priority=11
)


@remake.handle()
async def _(state: T_State = State()):
    life_ = Life()
    life_.load()
    talents = life_.rand_talents(10)
    state["life"] = life_
    state["talents"] = talents
    msg = "请发送编号选择3个天赋哦，如“0 1 2”；或发送“随机”随机选择√"
    des = "\n".join([f"{i}.{t}" for i, t in enumerate(talents)])
    await remake.send(f"{msg}\n\n{des}", at_sender=True)


@remake.got("nums")
async def _(reply: str = ArgPlainText("nums"), state: T_State = State()):
    def conflict_talents(talents: List[Talent]) -> Optional[Tuple[Talent, Talent]]:
        for (t1, t2) in itertools.combinations(talents, 2):
            if t1.exclusive_with(t2):
                return t1, t2
        return None

    life_: Life = state["life"]
    talents: List[Talent] = state["talents"]

    match = re.fullmatch(r"\s*(\d)\s*(\d)\s*(\d)\s*", reply)
    if match:
        nums = list(match.groups())
        nums = [int(n) for n in nums]
        nums.sort()
        if nums[-1] >= 10:
            await remake.reject("请发送正确的编号！！", at_sender=True)

        talents_selected = [talents[n] for n in nums]
        ts = conflict_talents(talents_selected)
        if ts:
            await remake.reject(f"你选择的天赋“{ts[0].name}”和“{ts[1].name}”不能同时拥有哦，请重新选择×", at_sender=True)
    elif reply == "随机":
        while True:
            nums = random.sample(range(10), 3)
            nums.sort()
            talents_selected = [talents[n] for n in nums]
            if not conflict_talents(talents_selected):
                break
    elif re.fullmatch(r"[\d\s]+", reply):
        await remake.reject("请发送正确的编号！！如“0 1 2”", at_sender=True)
    else:
        await remake.finish("你的人生重开已取消~", at_sender=True)

    life_.set_talents(talents_selected)
    state["talents_selected"] = talents_selected

    msg = (
        "请发送4个数字分配“颜值、智力、体质、家境”4个属性，如“5 5 5 5”，或发送“随机”随机选择；"
        f"可用属性点为{life_.total_property()}，每个属性不能超过10"
    )
    await remake.send(msg, at_sender=True)


@remake.got("prop")
async def _(
    bot: Bot,
    event: MessageEvent,
    reply: str = ArgPlainText("prop"),
    state: T_State = State(),
):
    life_: Life = state["life"]
    talents: List[Talent] = state["talents_selected"]
    total_prop = life_.total_property()

    match = re.fullmatch(r"\s*(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s*", reply)
    if match:
        nums = list(match.groups())
        nums = [int(n) for n in nums]
        if sum(nums) != total_prop:
            await remake.reject(f"属性之和需为{total_prop}，请重新发送！！", at_sender=True)
        elif max(nums) > 10:
            await remake.reject("每个属性不能超过10，请重新发送！！", at_sender=True)
    elif reply == "随机":
        half_prop1 = int(total_prop / 2)
        half_prop2 = total_prop - half_prop1
        num1 = random.randint(0, half_prop1)
        num2 = random.randint(0, half_prop2)
        nums = [num1, num2, half_prop1 - num1, half_prop2 - num2]
        random.shuffle(nums)
    elif re.fullmatch(r"[\d\s]+", reply):
        await remake.reject("请发送正确的数字！！如“5 5 5 5”", at_sender=True)
    else:
        await remake.finish("你的人生重开已取消×", at_sender=True)

    prop = {"CHR": nums[0], "INT": nums[1], "STR": nums[2], "MNY": nums[3]}
    life_.apply_property(prop)

    await remake.send("你的人生正在重开...", at_sender=True)

    msgs = [
        "已选择以下天赋：\n" + "\n".join([str(t) for t in talents]),
        "已设置如下属性：\n" + f"颜值{nums[0]} 智力{nums[1]} 体质{nums[2]} 家境{nums[3]}",
    ]
    try:
        life_msgs = []
        for s in life_.run():
            life_msgs.append("\n".join(s))
        n = 5
        life_msgs = [
            "\n\n".join(life_msgs[i : i + n]) for i in range(0, len(life_msgs), n)
        ]
        msgs.extend(life_msgs)
        msgs.append(life_.gen_summary())
        if isinstance(event, GroupMessageEvent):
            await send_forward_msg(bot, event, "雾子酱~人生重开√", bot.self_id, msgs)
        else:
            for msg in msgs:
                await remake.send(msg)
                await asyncio.sleep(2)
    except:
        logger.warning(traceback.format_exc())
        await remake.finish("你的人生重开失败...要再试一次吗×", at_sender=True)


async def send_forward_msg(
    bot: Bot,
    event: GroupMessageEvent,
    name: str,
    uin: str,
    msgs: List[str],
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )
