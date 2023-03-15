from pathlib import Path
from typing import Optional, Tuple

from .deal_json import load_json

path = Path.cwd() / "data" / "genshin_history" / "alias.json"


def get_name_by_alias(target: str, type: str) -> Optional[str]:
    """
    :param target: 别名
    :param type: 类型
    :return: 真正的名字
    """
    data = load_json(path)[f"{type}"]
    return next((k for k, v in data.items() if target in v), None)


def find_name(target: str) -> Optional[Tuple[str, Optional[str]]]:
    """
    :param target: 从用户输入获取到的名称/别名
    :return: 真正的名字, 类型[角色/武器]
    """
    types = {"type1": "角色", "type2": "武器"}
    result = None
    found_type = None
    for _ in range(2):
        for t in types.values():
            if (result := get_name_by_alias(target, t)) is not None:
                found_type = t
                break
        if result is not None:
            break
    return result, found_type
