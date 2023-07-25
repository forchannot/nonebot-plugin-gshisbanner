from nonebot.plugin import PluginMetadata

from .config import Config
from .main import *  # noqa: F403

__version__ = "0.6.1"
__plugin_meta__ = PluginMetadata(
    name="gshisbanner",
    description="这是一个在机器人上获取原神历史卡池的插件",
    usage="XX历史卡池,XX卡池(版本)，详细查看本仓库readme",
    type="application",
    homepage="https://github.com/forchannot/nonebot-plugin-gshisbanner",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={
        "author": "forchannot",
        "version": __version__,
    },
)
