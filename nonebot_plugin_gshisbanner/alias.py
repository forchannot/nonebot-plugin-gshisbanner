from typing import Dict, List, Optional, Tuple, cast

from .constant import alias_path
from .deal_json import load_json


def get_name_by_alias(target: str, target_type: str) -> Optional[str]:
    """
    :param target: 别名
    :param target_type: 类型
    :return: 真正的名字
    """
    data: Dict[str, List[str]] = cast(Dict, load_json(alias_path))[target_type]
    return next((k for k, v in data.items() if target in v), None)


def find_name(target: str) -> Tuple[Optional[str], str]:
    """
    :param target: 从用户输入获取到的名称/别名
    :return: 真正的名字, 类型[角色/武器] or None
    """
    types = ["角色", "武器"]
    result = None
    found_type = "None"
    for _ in range(2):
        for target_type in types:
            if (result := get_name_by_alias(target, target_type)) is not None:
                found_type = target_type
                break
        if result is not None:
            break
    return result, found_type
