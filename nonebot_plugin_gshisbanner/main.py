import contextlib
from pathlib import Path
from typing import Union

from nonebot import get_driver, logger
from nonebot.adapters.onebot.v11 import (
    GROUP_ADMIN,
    GROUP_OWNER,
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import Keyword
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_keyword

from .alias import find_name
from .api import get
from .config import plugin_config
from .deal import deal_info_from_name, deal_info_from_version, delete_command_start
from .deal_json import load_json_from_url, save_json
from .send import word_send_from_name, word_send_from_version

old_gacha = on_keyword(
    {"历史卡池", "历史up"},
    priority=45,
    block=True,
)
version_gacha = on_keyword(
    {"卡池", "up"},
    priority=47,
    block=False,
)
refresh = on_keyword(
    {"刷新", "更新"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=40,
    block=True,
)


DRIVER = get_driver()
gacha_info_path = Path.cwd() / "data" / "genshin_history"
special_version = ["1.3"]  # 特殊三卡池版本
forward_length = plugin_config.gshisbanner_forward_length  # 合并转发长度


@old_gacha.handle()
async def _(
    bot: Bot,
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    key: str = Keyword(),  # noqa: B008
):
    name, length = event.get_plaintext().split(key)
    name = delete_command_start(name)
    if name in ["刷新", "更新"]:
        return
    if length and not length.isdigit():
        return
    real_name, real_type = find_name(name)
    if real_name is None or real_type not in ["角色", "武器"]:
        await old_gacha.finish("该角色/武器不存在或是从未up过")
    # 获取up信息
    info = await deal_info_from_name(real_name, "cha" if real_type == "角色" else "wep")
    if length := int(length) if length else plugin_config.gshisbanner_forward_length:
        await word_send_from_name(bot, event, real_name, info, length)


@version_gacha.handle()
async def _(
    bot: Bot,
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    key: str = Keyword(),  # noqa: B008
):
    version, upordown = event.get_plaintext().split(key)
    version = delete_command_start(version)
    if version in ["刷新", "更新"]:
        return
    if upordown and not (
        upordown.isdigit() and all(part.isdigit() for part in version.split("."))
    ):
        return
    if upordown == "3" and version not in special_version:
        return
    real_version = f"{version}.{upordown}" if upordown else version
    if info := await deal_info_from_version(real_version, not upordown):
        await word_send_from_version(bot, event, real_version, info)


@refresh.handle()
async def _(
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    key: str = Keyword(),  # noqa: B008
):
    args = event.get_plaintext().split(key)
    _arg = delete_command_start(args[0])
    if _arg:
        return
    choose = args[1]
    if choose in ["历史卡池", "历史up", "卡池", "up"]:
        for i in ["character", "weapon"]:
            url = f"https://{plugin_config.gshisbanner_json_url}/{i}.json"
            path = gacha_info_path / f"{i}.json"
            result = await load_json_from_url(url, path, True)
            if not result:
                await refresh.send(f"刷新{i}.json失败,可能是网络问题或api失效")
                continue
            save_json(result, path)
            logger.info(f"{i}.json文件保存成功")
    elif choose == "别名":
        if (await init_group_card(True)) is False:
            await refresh.finish(f"刷新{choose}失败,可能是网络问题或api失效")
    await refresh.finish(f"刷新{choose}成功")


@DRIVER.on_startup
async def init_group_card(force_refresh: bool = False) -> bool:
    if not gacha_info_path.exists():
        gacha_info_path.mkdir(parents=True)
    urls = [
        "https://jsd.cdn.zzko.cn/gh/forchannot/nonebot-plugin-gshisbanner@main/data/genshin_history/alias.json",
        "https://raw.fastgit.org/forchannot/nonebot-plugin-gshisbanner/main/data/genshin_history/alias.json",
        "https://cdn.staticaly.com/gh/forchannot/nonebot-plugin-gshisbanner@main/data/genshin_history/alias.json",
        "https://fastly.jsdelivr.net/gh/forchannot/nonebot-plugin-gshisbanner@main/data/genshin_history/alias.json",
    ]
    if (gacha_info_path / "alias.json").exists() and not force_refresh:
        logger.info("alias.json文件已存在，跳过下载，如需更新请使用刷新别名功能")
        return False
    for url in urls:
        with contextlib.suppress(Exception):
            resp = await get(url, follow_redirects=True)
            if resp.status_code == 200:
                break
    else:
        logger.warning("alias.json文件下载失败")
        return False
    data = resp.json()
    save_json(data=data, path=gacha_info_path / "alias.json")
    logger.info("alias.json文件保存成功")
    return True
