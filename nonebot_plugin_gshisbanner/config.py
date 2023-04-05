# 插件的配置文件
from nonebot import get_driver
from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    gshisbanner_forward_length: int = 10


config = Config.parse_obj(get_driver().config.dict())