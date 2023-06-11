# 插件的配置文件
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    gshisbanner_forward_length: int = 10
    gshisbanner_json_url: str = "banners.52v6.com/data"


plugin_config = Config.parse_obj(get_driver().config.dict())
