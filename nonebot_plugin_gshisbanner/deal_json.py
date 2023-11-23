import json
from json import JSONDecodeError
from pathlib import Path
from typing import Dict, List, Union

from .api import get


def save_json(
    data: Union[Dict, List[Dict]], path: Union[Path, str], encoding: str = "utf-8"
):
    if isinstance(path, str):
        path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding=encoding)


def load_json(path: Union[Path, str], encoding: str = "utf-8") -> List[Dict]:
    if isinstance(path, str):
        path = Path(path)
    if not path.name.endswith(".json"):
        path = path.with_suffix(".json")
    return json.loads(path.read_text(encoding=encoding)) if path.exists() else [{}]


async def load_json_from_url(
    url: str, path: Union[Path, str], force: bool = False
) -> List[Dict]:
    if path and Path(path).exists() and not force:
        return load_json(path=path)
    resp = await get(url)
    if resp.status_code != 200:
        return [{}]
    try:
        data: List[Dict] = resp.json()
    except JSONDecodeError:
        return [{}]
    if path and not Path(path).exists():
        save_json(data=data, path=path)
    return data
