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
from .config import Config
from .deal import deal_info_from_name, deal_info_from_version
from .deal_json import load_json_from_url, save_json
from .send import word_send_from_name, word_send_from_version

old_gacha = on_regex(
    r"(?<!\w)(?P<name>[\u4e00-\u9fa5]+)(?<!刷新)(历史卡池|历史up)(?P<len>\d{0,2})(?!.)"
)
version_gacha = on_regex(r"(?<!.)(?P<version>\d\.\d)(卡池|up)(?P<upordown>(1|2|3)?)(?!.)")
refresh = on_regex(
    r"(?<!.)刷新(?P<name>历史卡池|别名)(?!.)",
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=13,
    block=False,
)

DRIVER = get_driver()
gacha_info_path = Path.cwd() / "data" / "genshin_history"
config = Config.parse_obj(get_driver().config.dict())


@old_gacha.handle()
async def _(
    bot: Bot,
    event: Union[GroupMessageEvent, PrivateMessageEvent],
    regex_dict: dict = RegexDict(),
):
    type_name = regex_dict["name"]
    if config.gshisbanner_forward_length <= 0:
        await old_gacha.finish("请不要将合并转发长度设为小于等于0的数字")
    # regex_dict["len"]：表示合并转发的长度,由用户输入获取，为获取到则为默认值
    length = (
        int(regex_dict["len"])
        if regex_dict["len"]
        else config.gshisbanner_forward_length
    )
    # 获取角色真实名字
    real_name, is_type = find_name(type_name)
    if real_name is None or is_type not in ["角色", "武器"]:
        await old_gacha.finish("该角色/武器不存在或是从未up过")
    # 获取up信息
    info = await deal_info_from_name(real_name, "cha" if is_type == "角色" else "wep")
    await word_send_from_name(bot, event, real_name, info, length)
    await old_gacha.finish()


@version_gacha.handle()
async def _(bot: Bot, event: MessageEvent, regex_dict: dict = RegexDict()):
    special_version = ["1.3"]  # 特殊版本
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
    info = await deal_info_from_version(
        real_version, False if regex_dict["upordown"] else True
    )
    if info is not None:
        await word_send_from_version(bot, event, real_version, info)
    await version_gacha.finish()


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
            result = await load_json_from_url(url, path, True)
            if not result:
                await refresh.finish("刷新失败,可能是网络问题或api失效")
            save_json(result, path)
            logger.info(f"{i}.json文件保存成功")
    elif type_name == "别名":
        await init_group_card(True)
    await refresh.finish(f"刷新{type_name}成功")


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
        logger.info("alias.json文件保存成功")
