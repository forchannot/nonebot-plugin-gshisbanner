# 插件的配置文件
from typing import Literal

from nonebot import get_driver
from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    gshisbanner_forward_length: int = 10
    """单次合并转发条数"""
    gshisbanner_json_url: str = "banners.52v6.com/data"
    """卡池信息来源网站"""
    send_type: Literal["forward", "pic"] = "forward"
    """发送方式：[“合并转发”，“图片”]"""
    pic_font_path: str = "msyh.ttc"
    """图片字体路径"""


plugin_config = Config.parse_obj(get_driver().config.dict())
