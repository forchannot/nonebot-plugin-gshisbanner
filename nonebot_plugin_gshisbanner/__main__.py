from datetime import datetime
from pathlib import Path
from typing import Union

from nonebot import on_regex, get_driver, logger
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    Bot,
    GROUP_ADMIN,
    GROUP_OWNER,
)
from nonebot.params import RegexDict
from nonebot.permission import SUPERUSER

from .alias import find_name
from .api import get
from .deal import deal_info
from .deal_json import load_json_from_url, save_json

old_gacha = on_regex(r"(?P<name>[\u4e00-\u9fa5]+)(?<!刷新)历史卡池")
refresh = on_regex(
    r"刷新(?P<name>历史卡池|别名)",
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=13,
    block=False,
)

DRIVER = get_driver()
NICKNAME: str = (
    list(DRIVER.config.nickname)[0] if list(DRIVER.config.nickname) else "BOT"
)
gacha_info_path = Path.cwd() / "data" / "genshin_history"


@old_gacha.handle()
async def _(
    bot: Bot,
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    regex_dict: dict = RegexDict(),
):
    msg = []
    type_name = regex_dict["name"]
    real_name, is_type = find_name(type_name)
    if real_name is None or is_type not in ["角色", "武器"]:
        await old_gacha.finish("该角色/武器不存在或是从未up过")
    info = await deal_info(real_name, "cha" if is_type == "角色" else "wep")
    end_time = datetime.strptime(info[0]["end"], "%Y-%m-%d %H:%M:%S").date()
    end_t = (datetime.now().date() - end_time).days
    delta_time = f"最近一次up距离现在已有{end_t}天" if end_t > 0 else f"当前正在up中,距离结束还有约{-end_t}天"
    msg.append(
        {
            "type": "node",
            "data": {
                "name": NICKNAME,
                "uin": event.self_id,
                "content": f"{real_name}{delta_time}",
            },
        }
    )
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


@refresh.handle()
async def _(
    event: MessageEvent,
    regex_dict: dict = RegexDict(),
):
    type_name = regex_dict["name"]
    types = ["character", "weapon"]
    if type_name == "历史卡池":
        for i in types:
            url = f"https://genshin-gacha-banners.52v6.com/data/{i}.json"
            path = Path.cwd() / "data" / "genshin_history" / f"{i}.json"
            result = await load_json_from_url(url, path)
            if not result:
                await refresh.finish("刷新失败,可能是网络问题或api失效")
            save_json(result, path)
    elif type_name == "别名":
        await init_group_card(True)
    await refresh.finish("刷新成功")


@DRIVER.on_startup
async def init_group_card(force: bool = True):
    path = Path.cwd() / "data" / "genshin_history"
    if not path.exists():
        path.mkdir(parents=True)
    if force:
        url = "https://raw.gitmirror.com/forchannot/nonebot-plugin-gshisbanner/master/data/genshin_history/alias.json"
        resp = await get(url)
        data = resp.json()
        save_json(data=data, path=path / "alias.json")
        logger.info("alias文件保存成功")
