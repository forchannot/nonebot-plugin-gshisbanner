from pathlib import Path

from nonebot import get_driver

from .config import plugin_config

DRIVER = get_driver()

gacha_info_path = Path.cwd() / "data" / "genshin_history"
alias_path = Path.cwd() / "data" / "genshin_history" / "alias.json"
history_path = Path.cwd() / "data" / "genshin_history"

special_version = ["1.3"]  # 特殊三卡池版本

forward_length = plugin_config.gshisbanner_forward_length
command_start = get_driver().config.command_start
