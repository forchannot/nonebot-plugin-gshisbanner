# 插件的配置文件
from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    gshisbanner_forward_length: int = 10
    """单次合并转发条数"""
    gshisbanner_json_url: str = "banners.52v6.com/data"
    """卡池信息来源网站"""


plugin_config = Config.parse_obj(get_driver().config.dict())
