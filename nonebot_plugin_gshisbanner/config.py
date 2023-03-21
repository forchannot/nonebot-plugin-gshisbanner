# 插件的配置文件
from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    gshisbanner_forward_length: int = 10