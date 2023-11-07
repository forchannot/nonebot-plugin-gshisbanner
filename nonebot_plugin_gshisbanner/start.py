import contextlib
from typing import Dict

from nonebot import logger

from .api import get
from .constant import DRIVER, gacha_info_path
from .deal_json import save_json


@DRIVER.on_startup
async def init_group_card(force_refresh: bool = False) -> bool:
    if not gacha_info_path.exists():
        gacha_info_path.mkdir(parents=True)
    urls = [
        "jsd.zhenxun.buzz",  # 作者自己的转发，不保证稳定性
        "cdn.jsdelivr.net",
        "jsd.cdn.zzko.cn",
        "fastly.jsdelivr.net",
    ]
    url_base = (
        "gh/forchannot/nonebot-plugin-gshisbanner@main/data/genshin_history/alias.json"
    )
    if (gacha_info_path / "alias.json").exists() and not force_refresh:
        logger.info("alias.json文件已存在，跳过下载，如需更新请使用刷新别名功能")
        return False
    for url in urls:
        url = f"https://{url}/{url_base}"
        with contextlib.suppress(Exception):
            resp = await get(url, follow_redirects=True)
            if resp.status_code == 200:
                break
    else:
        logger.warning("alias.json文件下载失败")
        return False
    data: Dict = resp.json()
    save_json(data=data, path=gacha_info_path / "alias.json")
    logger.info("alias.json文件保存成功")
    return True
