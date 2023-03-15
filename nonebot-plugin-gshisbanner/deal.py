from pathlib import Path

from .deal_json import load_json_from_url

path = Path.cwd() / "data" / "genshin_history"


async def get_info_from_url(cha: bool, cache_dir: Path = path):
    """
    :param cha: 类型
    :param cache_dir: 本地缓存
    :return: dict
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    if cha:
        url = "https://genshin-gacha-banners.52v6.com/data/character.json"
        cache_path = cache_dir / "character.json"
    else:
        url = "https://genshin-gacha-banners.52v6.com/data/weapon.json"
        cache_path = cache_dir / "weapon.json"
    return await load_json_from_url(url, path=cache_path)


async def deal_info(name: str, choose: str):
    """
    :param name: 名字
    :param choose: 类型
    :return: 获取到的历史卡池数据
    """
    result = []
    if choose == "cha":
        jsons = await get_info_from_url(True)
        for data in jsons:
            for item in data["items"]:
                if item["name"] == name:
                    temp = {"start": data["start"], "end": data["end"]}
                    await deal_character_info(temp, data["items"], result)
    elif choose == "wep":
        jsons = await get_info_from_url(False)
        for data in jsons:
            for item in data["items"]:
                if item["name"] == name:
                    temp = {"start": data["start"], "end": data["end"]}
                    await deal_weapon_info(temp, data["items"], result)
    return result


async def deal_character_info(temp: dict, item: list, result: list):
    temp["five_character"] = [x["name"] for x in item if x.get("rankType") == 5]
    temp["four_character"] = [x["name"] for x in item if x.get("rankType") == 4]
    result.append(temp)


async def deal_weapon_info(temp: dict, item: list, result: list):
    temp["five_weapon"] = [x["name"] for x in item if x.get("rankType") == 5]
    temp["four_weapon"] = [x["name"] for x in item if x.get("rankType") == 4]
    result.append(temp)