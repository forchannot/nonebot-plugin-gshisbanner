# 插件的配置文件
from pydantic import Extra, BaseModel


class Config(BaseModel, extra=Extra.ignore):
    forward_length: int = 10