from datetime import datetime

from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot import get_driver


DRIVER = get_driver()
NICKNAME: str = (
    list(DRIVER.config.nickname)[0] if list(DRIVER.config.nickname) else "BOT"
)


# 历史卡池文字合并转发
async def word_send(bot, event, real_name, delta_time, info):
    msg = [
        {
            "type": "node",
            "data": {
                "name": NICKNAME,
                "uin": event.self_id,
                "content": f"{real_name}{delta_time}",
            },
        }
    ]
    for i in info:
        start = datetime.strptime(i["start"], "%Y-%m-%d %H:%M:%S").date()
        end = datetime.strptime(i["end"], "%Y-%m-%d %H:%M:%S").date()
        banner_five = (
            " ".join(i["five_character"])
            if i.get("five_character")
            else " ".join(i["five_weapon"])
        )
        banner_four = (
            " ".join(i["four_character"])
            if i.get("four_character")
            else " ".join(i["four_weapon"])
        )
        msg.append(
            {
                "type": "node",
                "data": {
                    "name": NICKNAME,
                    "uin": event.self_id,
                    "content": f"五星：{banner_five}\n四星：{banner_four}\nup时间：\n{start}~~{end}",
                },
            }
        )
    if isinstance(event, GroupMessageEvent):
        await bot.call_api(
            "send_group_forward_msg",
            group_id=event.group_id,
            messages=msg,
        )
    elif isinstance(event, PrivateMessageEvent):
        await bot.call_api(
            "send_private_forward_msg",
            user_id=event.user_id,
            messages=msg,
        )
