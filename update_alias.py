import json
import re
from pathlib import Path

import requests

urls = {
    "角色": "https://raw.githubusercontent.com/yoimiya-kokomi/miao-plugin/master/resources/meta-gs/character/alias.js",
    "武器": "https://raw.githubusercontent.com/yoimiya-kokomi/miao-plugin/master/resources/meta-gs/weapon/alias.js",
}

result_dict = {"角色": {}, "武器": {}}

for alias_type, url in urls.items():
    js_text = requests.get(url).text
    match = re.search(r"export const alias = {(.*?)}", js_text, re.DOTALL)
    if match:
        js_text = match.group(1)
        lines = js_text.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("/") or not line:
                continue
            key, value = line.split(":")
            key = key.strip()
            value = value.strip().strip(",").strip("'")
            result_dict[alias_type][key] = value.split(",")

        with open(
            Path("./data/genshin_history/alias.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
