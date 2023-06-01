from nonebot.plugin import PluginMetadata

from .main import *  # noqa

__version__ = "0.5.2"
__plugin_meta__ = PluginMetadata(
    name="gshisbanner",
    description="这是一个在机器人上获取原神历史卡池的插件",
    usage="XX历史卡池,XX版本卡池，详细查看本仓库readme",
    type="application",
    homepage="https://github.com/forchannot/nonebot-plugin-gshisbanner",
    supported_adapters={"~onebot.v11"},
    extra={
        "author": "forchannot",
        "version": __version__,
    }
)
