from datetime import datetime

from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot import get_driver

from .config import Config

DRIVER = get_driver()
NICKNAME: str = (
    list(DRIVER.config.nickname)[0] if list(DRIVER.config.nickname) else "BOT"
)
config = Config.parse_obj(get_driver().config.dict())


# 历史卡池文字合并转发
async def word_send(bot, event, real_name, info, length):
    end_time = datetime.strptime(info[0]["end"], "%Y-%m-%d %H:%M:%S").date()
    end_t = (datetime.now().date() - end_time).days
    delta_time = f"最近一次up距离现在已有{end_t}天" if end_t > 0 else f"当前正在up中,距离结束还有约{-end_t}天"
    msg1 = [
        {
            "type": "node",
            "data": {
                "name": NICKNAME,
                "uin": event.self_id,
                "content": f"{real_name}{delta_time}",
            },
        }
    ]
    for i in range(0, len(info), length):
        msg = msg1.copy() if i == 0 else []
        for j in info[i: i + length]:
            start = datetime.strptime(j["start"], "%Y-%m-%d %H:%M:%S").date()
            end = datetime.strptime(j["end"], "%Y-%m-%d %H:%M:%S").date()
            version = "{}.{}  卡池{}".format(*j["version"].split("."))
            banner_five = (
                " ".join(j["five_character"])
                if j.get("five_character")
                else " ".join(j["five_weapon"])
            )
            banner_four = (
                " ".join(j["four_character"])
                if j.get("four_character")
                else " ".join(j["four_weapon"])
            )
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
