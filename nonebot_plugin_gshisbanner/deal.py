from pathlib import Path
from typing import Dict, List, Union

from .config import plugin_config
from .constant import command_start, history_path
from .deal_json import load_json_from_url
from .model import GsGacha


async def get_info_from_url(cha: bool, cache_dir: Path = history_path) -> List[Dict]:
    """
    :param cha: 类型
    :param cache_dir: 本地缓存
    :return: list[dict]
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    url = f"https://{plugin_config.gshisbanner_json_url}/{'character' if cha else 'weapon'}.json"
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
    all_data = await get_info_from_url(choose == "cha")
    if not all_data:
        return result
    obj_datas = [GsGacha.parse_obj(data) for data in all_data]
    for obj_data in obj_datas:
        obj_data_items = obj_data.items
        if any(x.name == name for x in obj_data_items):
            temp: Dict[str, Union[str, List[str]]] = {
                "start": obj_data.start,
                "end": obj_data.end,
                "version": obj_data.version,
            }
            if choose == "cha":
                temp["five_character"] = [
                    x.name for x in obj_data_items if x.rankType == 5
                ]
                temp["four_character"] = [
                    x.name for x in obj_data_items if x.rankType == 4
                ]
            else:
                temp["five_weapon"] = [
                    x.name for x in obj_data_items if x.rankType == 5
                ]
                temp["four_weapon"] = [
                    x.name for x in obj_data_items if x.rankType == 4
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
    # 获取所有卡池信息
    gacha_data_cha: List[Dict] = await get_info_from_url(True)
    gacha_data_wep: List[Dict] = await get_info_from_url(False)
    gacha_data_all: List[Dict] = gacha_data_cha + gacha_data_wep
    if not gacha_data_all:
        return []
    # 卡池类型列表
    type_list: List[str] = [
        "five_character",
        "four_character",
        "five_weapon",
        "four_weapon",
    ]
    result = []
    obj_datas = [GsGacha.parse_obj(data) for data in gacha_data_all]
    for obj_data in obj_datas:
        obj_data_items = obj_data.items
        # 判断是否为指定版本
        if obj_data.version[:3] == version if is_all else obj_data.version == version:
            # 构造卡池信息字典
            temp: Dict[str, Union[str, List[str]]] = {
                "start": obj_data.start,
                "end": obj_data.end,
                "version": obj_data.version,
            }
            # 遍历卡池类型列表
            for type in type_list:
                temp[type] = [
                    x.name
                    for x in obj_data_items
                    if x.rankType == (5 if "five" in type else 4)
                    and x.itemType == type.split("_")[1].capitalize()
                ]
            result.append(temp)
    return [{k: v for k, v in data.items() if v} for data in result]


def delete_command_start(text: str) -> str:
    """
    :param text: 原始文本
    :return: 删除文本开头的指令符
    """
    return text[1:] if any(text.startswith(cs) for cs in command_start if cs) else text
