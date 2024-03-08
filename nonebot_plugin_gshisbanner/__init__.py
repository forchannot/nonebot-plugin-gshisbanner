from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_saa")
from nonebot_plugin_saa import enable_auto_select_bot

from .config import Config
from .constant import DRIVER
from .adapters import *  # noqa: F401, F403
from .start import init_group_card  # noqa: F401

enable_auto_select_bot()
DRIVER.on_startup(init_group_card)

__version__ = "1.2.5"
__plugin_meta__ = PluginMetadata(
    name="gshisbanner",
    description="这是一个在机器人上获取原神历史卡池的插件",
    usage="""
    (
        usage1: [角色/武器名]历史卡池/历史up[长度],
        explain1: 获取该角色/武器的历史卡池信息,
        example1: [莫娜历史卡池，刻晴历史up6]
    ),
    (
        usage2: [版本号]卡池/up,
        explain2: 获取该版本的卡池信息,
        example2: [1.3卡池,1.4up,4.0.1up]
    ),
    (
        usage3: [刷新/更新]历史卡池/别名,
        explain3: 刷新历史卡池信息或者刷新别名,
        example3: [刷新历史卡池,更新别名]
    )
    """,
    type="application",
    homepage="https://github.com/forchannot/nonebot-plugin-gshisbanner",
    config=Config,
    supported_adapters={"~onebot.v11", "~red"},
    extra={
        "author": "forchannot",
        "version": __version__,
    },
)
