from datetime import datetime

from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot import get_driver

DRIVER = get_driver()
NICKNAME: str = (
    list(DRIVER.config.nickname)[0] if list(DRIVER.config.nickname) else "BOT"
)


# 角色历史卡池文字合并转发预处理
async def word_send_from_name(bot, event, real_name, info, length):
    end_time = datetime.strptime(info[0]["end"], "%Y-%m-%d %H:%M:%S").date()
    end_t = (datetime.now().date() - end_time).days
    delta_time = f"最近一次up距离现在已有{end_t}天" if end_t > 0 else f"当前正在up中,距离结束还有约{-end_t}天"
    msg_content = f"{real_name}{delta_time}"
    for i in range(0, len(info), length):
        if i == 0:
            msg = msg_content
        else:
            msg = []
        await send_banner_info(bot, event, msg, info[i: i + length])


# 版本卡池文字合并转发预处理
async def word_send_from_version(bot, event, version, info):
    msg_content = f"{version}版本卡池"
    await send_banner_info(bot, event, msg_content, info)


# 合并转发
async def send_forward_msg(bot, event, info):
    if isinstance(event, GroupMessageEvent):
        await bot.call_api(
            "send_group_forward_msg",
            group_id=event.group_id,
            messages=info,
        )
    elif isinstance(event, PrivateMessageEvent):
        await bot.call_api(
            "send_private_forward_msg",
            user_id=event.user_id,
            messages=info,
        )


# 合并转发最终处理
async def send_banner_info(bot, event, msg_content, banner_info):
    msg = [
        {
            "type": "node",
            "data": {
                "name": NICKNAME,
                "uin": event.self_id,
                "content": msg_content,
            },
        }
    ]
    for info in banner_info:
        start = datetime.strptime(info["start"], "%Y-%m-%d %H:%M:%S").date()
        end = datetime.strptime(info["end"], "%Y-%m-%d %H:%M:%S").date()
        version = "{}.{}  卡池{}".format(*info["version"].split("."))
        banner_five = " ".join(info.get("five_character", info.get("five_weapon", [])))
        banner_four = " ".join(info.get("four_character", info.get("four_weapon", [])))
        msg.append(
            {
                "type": "node",
                "data": {
                    "name": NICKNAME,
                    "uin": event.self_id,
                    "content": f"版本：{version}\n五星：{banner_five}\n四星：{banner_four}\nup时间：\n{start}~~{end}",
                },
            }
        )
    await send_forward_msg(bot, event, msg)