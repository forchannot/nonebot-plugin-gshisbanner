from datetime import datetime

from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent
from nonebot import get_driver

from .config import Config

DRIVER = get_driver()
NICKNAME: str = (
    list(DRIVER.config.nickname)[0] if list(DRIVER.config.nickname) else "BOT"
)
config = Config.parse_obj(get_driver().config.dict())


# 角色历史卡池文字合并转发处理
async def word_send_from_name(bot, event, real_name, info, length):
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
    # 根据用户输入长度，循环每个卡池，分次发送
    for i in range(0, len(info), length):
        msg = msg1.copy() if i == 0 else []
        # 循环每个卡池，判断是否与用户输入的名称相同
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
        await send_forward_msg(bot, event, msg)


# 版本卡池文字合并转发处理
async def word_send_from_version(bot, event, version, info):
    msg1 = [
        {
            "type": "node",
            "data": {
                "name": NICKNAME,
                "uin": event.self_id,
                "content": f"{version}版本卡池",
            },
        }
    ]
    # 循环每个卡池，判断是否与用户输入的版本号相同
    for j in info:
        start = datetime.strptime(j["start"], "%Y-%m-%d %H:%M:%S").date()
        end = datetime.strptime(j["end"], "%Y-%m-%d %H:%M:%S").date()
        version = "{}.{}  卡池{}".format(*j["version"].split("."))
        banner_five = (
            " ".join(j["five_character"])
            if j["five_character"]
            else " ".join(j["five_weapon"])
        )
        banner_four = (
            " ".join(j["four_character"])
            if j["four_character"]
            else " ".join(j["four_weapon"])
        )
        msg1.append(
            {
                "type": "node",
                "data": {
                    "name": NICKNAME,
                    "uin": event.self_id,
                    "content": f"版本：{version}\n五星：{banner_five}\n四星：{banner_four}\nup时间：\n{start}~~{end}",
                },
            }
        )
    await send_forward_msg(bot, event, msg1)


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
