from pathlib import Path
from typing import Union, List, Dict

from .deal_json import load_json_from_url
from .config import config

path = Path.cwd() / "data" / "genshin_history"


async def get_info_from_url(
    cha: bool, cache_dir: Path = path
) -> Union[Dict, List[Dict]]:
    """
    :param cha: 类型
    :param cache_dir: 本地缓存
    :return: Union[dict, list[dict]]
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://{config.gshisbanner_json_url}/{'character' if cha else 'weapon'}.json"
    cache_path = cache_dir / ("character.json" if cha else "weapon.json")
    return await load_json_from_url(url, path=cache_path)


async def deal_info_from_name(
    name: str, choose: str
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    :param name: 名字
    :param choose: 类型
    :return: 获取到的历史卡池数据
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


async def deal_info_from_version(
    version: str, is_all: bool
) -> List[Dict[str, Union[str, List[str]]]]:
    """
    :param version: 版本号
    :param is_all: 是否获取全部卡池
    :return: 获取到的历史卡池数据
    """
    json = await get_info_from_url(True) + await get_info_from_url(False)  # type: ignore
    type_list = ["five_character", "four_character", "five_weapon", "four_weapon"]
    result = []
    for data in json:
        if data["version"][:3] == version if is_all else data["version"] == version:
            result.append(
                {
                    "start": data["start"],
                    "end": data["end"],
                    # 利用 zip 将 type_list 和得到的对应值的列表合并成一个元组，其中 type_list 作为键，得到的列表作为值,最后将元组转换成字典
                    **dict(
                        zip(
                            type_list,
                            (
                                [
                                    x["name"]
                                    for x in data["items"]
                                    if x.get("rankType") == (5 if "five" in item else 4)
                                    and x.get("itemType")
                                    == item.split("_")[1].capitalize()
                                ]
                                for item in type_list
                            ),
                        )
                    ),
                    "version": data["version"],
                }
            )
    return [{k: v for k, v in data.items() if v} for data in result]
