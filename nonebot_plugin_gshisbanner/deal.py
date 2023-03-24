from pathlib import Path
from typing import Union

from .deal_json import load_json_from_url

path = Path.cwd() / "data" / "genshin_history"


async def get_info_from_url(cha: bool, cache_dir: Path = path) -> Union[dict, list[dict]]:
    """
    :param cha: 类型
    :param cache_dir: 本地缓存
    :return: Union[dict, list[dict]]
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    url = (
        "https://genshin-gacha-banners.52v6.com/data/character.json"
        if cha
        else "https://genshin-gacha-banners.52v6.com/data/weapon.json"
    )
    cache_path = cache_dir / ("character.json" if cha else "weapon.json")
    return await load_json_from_url(url, path=cache_path)


async def deal_info_from_name(name: str, choose: str) -> list[dict]:
    """
    :param name: 名字
    :param choose: 类型
    :return: list[dict]:获取到的历史卡池数据
    """
    result = []
    jsons = (
        await get_info_from_url(True)
        if choose == "cha"
        else await get_info_from_url(False)
    )
    for data in jsons:
        for item in data["items"]:
            if item["name"] == name:
                temp = {
                    "start": data["start"],
                    "end": data["end"],
                    "version": data["version"],
                }
                if choose == "cha":
                    temp["five_character"] = [
                        x["name"] for x in data["items"] if x.get("rankType") == 5
                    ]
                    temp["four_character"] = [
                        x["name"] for x in data["items"] if x.get("rankType") == 4
                    ]
                else:
                    temp["five_weapon"] = [
                        x["name"] for x in data["items"] if x.get("rankType") == 5
                    ]
                    temp["four_weapon"] = [
                        x["name"] for x in data["items"] if x.get("rankType") == 4
                    ]
                result.append(temp)
    return result


async def deal_info_from_version(version: str, is_all: bool) -> list[dict]:
    """
    :param version: 版本号
    :param is_all: 是否获取全部卡池
    :return: list[dict]:获取到的历史卡池数据
    """
    result = []
    json = await get_info_from_url(True) + await get_info_from_url(False)
    for data in json:
        if data["version"][:3] == version if is_all else data["version"] == version:
            temp = {
                "start": data["start"],
                "end": data["end"],
                "five_character": [
                    x["name"]
                    for x in data["items"]
                    if x.get("rankType") == 5 and x.get("itemType") == "Character"
                ],
                "four_character": [
                    x["name"]
                    for x in data["items"]
                    if x.get("rankType") == 4 and x.get("itemType") == "Character"
                ],
                "five_weapon": [
                    x["name"]
                    for x in data["items"]
                    if x.get("rankType") == 5 and x.get("itemType") == "Weapon"
                ],
                "four_weapon": [
                    x["name"]
                    for x in data["items"]
                    if x.get("rankType") == 4 and x.get("itemType") == "Weapon"
                ],
                "version": data["version"],
            }
            result.append(temp)
    return result or None
