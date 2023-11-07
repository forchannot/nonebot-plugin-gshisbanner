from datetime import datetime
from typing import Union

from nonebot import require

require("nonebot_plugin_saa")
from nonebot_plugin_saa import (
    AggregatedMessageFactory,
    MessageFactory,
    PlatformTarget,
    Text,
)

Sendable = Union[MessageFactory, AggregatedMessageFactory]


# 角色历史卡池文字合并转发预处理
async def word_send_from_name(
    send_target: PlatformTarget, real_name: str, info, length
):
    end_time = datetime.strptime(info[0]["end"], "%Y-%m-%d %H:%M:%S").date()
    start_time = datetime.strptime(info[0]["start"], "%Y-%m-%d %H:%M:%S").date()
    end_t = (datetime.now().date() - end_time).days
    start_t = (datetime.now().date() - start_time).days
    if end_t > 0:
        delta_time = f"最近一次up距离现在已有{end_t}天"
    elif start_t < 0:
        delta_time = f"还未开始up,距离开始还有约{-start_t}天"
    else:
        delta_time = (
            "当前还剩最后一天up了"
            if end_t == 0
            else f"当前正在up中,距离结束还有约{-end_t}天"
        )
    msg_content = f"{real_name}{delta_time}"
    for i in range(0, len(info), length):
        msg = msg_content if i == 0 else []
        await send_banner_info(send_target, msg, info[i : i + length])


# 版本卡池文字合并转发预处理
async def word_send_from_version(send_target: PlatformTarget, version, info):
    msg_content = f"{version}版本卡池"
    await send_banner_info(send_target, msg_content, info)


# 合并转发
async def send_forward_msg(send_target: PlatformTarget, info: Sendable):
    await info.send_to(send_target)


# 合并转发最终处理
async def send_banner_info(send_target: PlatformTarget, msg_content, banner_info):
    msgs = MessageFactory([Text(msg_content)])
    for info in banner_info:
        start = datetime.strptime(info["start"], "%Y-%m-%d %H:%M:%S").date()
        end = datetime.strptime(info["end"], "%Y-%m-%d %H:%M:%S").date()
        version = "{}.{}  卡池{}".format(*info["version"].split("."))
        banner_five = " ".join(info.get("five_character", info.get("five_weapon", [])))
        banner_four = " ".join(info.get("four_character", info.get("four_weapon", [])))
        msgs.append(
            f"版本：{version}\n五星：{banner_five}"
            f"\n四星：{banner_four}\nup时间：\n{start}~~{end}"
        )
    forward_msg = AggregatedMessageFactory(list(msgs))
    await send_forward_msg(send_target, forward_msg)
