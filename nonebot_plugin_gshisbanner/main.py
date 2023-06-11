import contextlib
from pathlib import Path
from typing import Union

from nonebot import get_driver, logger, on_regex
from nonebot.adapters.onebot.v11 import (
    GROUP_ADMIN,
    GROUP_OWNER,
    Bot,
    GroupMessageEvent,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import RegexDict
from nonebot.permission import SUPERUSER

from .alias import find_name
from .api import get
from .config import plugin_config
from .deal import deal_info_from_name, deal_info_from_version
from .deal_json import load_json_from_url, save_json
from .send import word_send_from_name, word_send_from_version

old_gacha = on_regex(
    r"(?<!\w)(?P<name>[\u4e00-\u9fa5]+)(?<!刷新)(历史卡池|历史up)(?P<len>\d{0,2})(?!.)",
    priority=35,
    block=False,
)
version_gacha = on_regex(
    r"(?<!.)(?P<version>\d\.\d)(卡池|up)(?P<upordown>(1|2|3)?)(?!.)",
    priority=35,
    block=False,
)
refresh = on_regex(
    r"(?<!.)(刷新|更新)(?P<name>历史卡池|别名)(?!.)",
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=13,
    block=False,
)

DRIVER = get_driver()
gacha_info_path = Path.cwd() / "data" / "genshin_history"
special_version = ["1.3"]  # 特殊三卡池版本
forward_length = plugin_config.gshisbanner_forward_length  # 合并转发长度


@old_gacha.handle()
async def _(
    bot: Bot,
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    regex_dict: dict = RegexDict(),  # noqa: B008
):
    type_name = regex_dict["name"]
    if not isinstance(forward_length, int) or forward_length <= 0:
        await old_gacha.finish("合并转发长度设置错误")
    # regex_dict["len"]：表示合并转发的长度,由用户输入获取，未获取到则为默认值
    length = (
        int(regex_dict["len"])
        if regex_dict["len"]
        else plugin_config.gshisbanner_forward_length
    )
    # 获取角色真实名字
    real_name, real_type = find_name(type_name)
    if real_name is None or real_type not in ["角色", "武器"]:
        await old_gacha.finish("该角色/武器不存在或是从未up过")
    # 获取up信息
    info = await deal_info_from_name(real_name, "cha" if real_type == "角色" else "wep")
    if length > 0:
        await word_send_from_name(bot, event, real_name, info, length)
    await old_gacha.finish()


@version_gacha.handle()
async def _(
    bot: Bot, event: MessageEvent, regex_dict: dict = RegexDict()  # noqa: B008
):  # noqa: B008
    # 判断是否为三卡池的版本
    if regex_dict["version"] not in special_version and regex_dict["upordown"] == "3":
        await version_gacha.finish()
    # 获取版本信息
    real_version = (
        f"{regex_dict['version']}.{regex_dict['upordown']}"
        if regex_dict["upordown"]
        else regex_dict["version"]
    )
    # 根据版本获取up信息
    info = await deal_info_from_version(real_version, not regex_dict["upordown"])
    if info:
        await word_send_from_version(bot, event, real_version, info)
    await version_gacha.finish()


@refresh.handle()
async def _(
    event: MessageEvent,
    regex_dict: dict = RegexDict(),  # noqa: B008
):
    type_name = regex_dict["name"]
    types = ["character", "weapon"]
    if type_name == "历史卡池":
        for i in types:
            url = f"https://{plugin_config.gshisbanner_json_url}/{i}.json"
            path = gacha_info_path / f"{i}.json"
            result = await load_json_from_url(url, path, True)
            if not result:
                await refresh.finish(f"刷新{type_name}失败,可能是网络问题或api失效")
            save_json(result, path)
            logger.info(f"{i}.json文件保存成功")
    elif type_name == "别名":
        if (await init_group_card(True)) is False:
            await refresh.finish(f"刷新{type_name}失败,可能是网络问题或api失效")
    await refresh.finish(f"刷新{type_name}成功")


@DRIVER.on_startup
async def init_group_card(force_refresh: bool = False) -> bool:
    if not gacha_info_path.exists():
        gacha_info_path.mkdir(parents=True)
    urls = [
        "https://jsd.cdn.zzko.cn/gh/forchannot/nonebot-plugin-gshisbanner@main/data/genshin_history/alias.json",
        "https://raw.fastgit.org/forchannot/nonebot-plugin-gshisbanner/main/data/genshin_history/alias.json",
        "https://cdn.jsdelivr.net/gh/forchannot/nonebot-plugin-gshisbanner@main/data/genshin_history/alias.json",
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
