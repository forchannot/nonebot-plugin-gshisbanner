from nonebot import logger, require
from nonebot.params import Keyword
from nonebot.permission import SUPERUSER
from nonebot.plugin.on import on_keyword

require("nonebot_plugin_saa")
from nonebot_plugin_saa import SaaTarget

from ..alias import find_name
from ..config import plugin_config
from ..constant import gacha_info_path, special_version
from ..deal import deal_info_from_name, deal_info_from_version, delete_command_start
from ..deal_json import load_json_from_url, save_json
from ..send import word_send_from_name, word_send_from_version
from ..start import init_group_card

old_gacha = on_keyword(
    {"历史卡池", "历史up"},
    priority=45,
    block=True,
)
version_gacha = on_keyword(
    {"卡池", "up"},
    priority=47,
    block=False,
)
refresh = on_keyword(
    {"刷新", "更新"},
    permission=SUPERUSER,
    priority=40,
    block=True,
)


try:
    from nonebot.adapters.red.event import MessageEvent as RedMessageEvent

    @old_gacha.handle()
    async def _(
        event: RedMessageEvent,
        target: SaaTarget,
        key: str = Keyword(),  # noqa: B008
    ):
        name, length = event.get_plaintext().split(key, 1)
        name = delete_command_start(name)
        if name in ["刷新", "更新"]:
            return
        if length and not length.isdigit():
            return
        real_name, real_type = find_name(name)
        if real_name is None or real_type not in ["角色", "武器"]:
            await old_gacha.finish("该角色/武器不存在或是从未up过")
        # 获取up信息
        info = await deal_info_from_name(
            real_name, "cha" if real_type == "角色" else "wep"
        )
        if not info:
            await old_gacha.finish("获取历史卡池信息失败，请联系超管")
        if (
            length := int(length)
            if length
            else plugin_config.gshisbanner_forward_length
        ):
            await word_send_from_name(target, real_name, info, length)

    @version_gacha.handle()
    async def _(
        event: RedMessageEvent,
        target: SaaTarget,
        key: str = Keyword(),  # noqa: B008
    ):
        version, upordown = event.get_plaintext().split(key, 1)
        version = delete_command_start(version)
        if version in ["刷新", "更新"]:
            return
        if upordown and not (
            upordown.isdigit() and all(part.isdigit() for part in version.split("."))
        ):
            return
        if upordown == "3" and version not in special_version:
            return
        real_version = f"{version}.{upordown}" if upordown else version
        if info := await deal_info_from_version(real_version, not upordown):
            if not info:
                await version_gacha.finish("获取历史卡池信息失败，请联系超管")
            await word_send_from_version(target, real_version, info)

    @refresh.handle()
    async def _(
        event: RedMessageEvent,
        key: str = Keyword(),  # noqa: B008
    ):
        args = event.get_plaintext().split(key, 1)
        if _arg := delete_command_start(args[0]):
            # 去除掉命令开头如果仍然有内容则不处理
            return
        choose = args[1]
        if choose in ["历史卡池", "历史up", "卡池", "up"]:
            for i in ["character", "weapon"]:
                url = f"https://{plugin_config.gshisbanner_json_url}/{i}.json"
                path = gacha_info_path / f"{i}.json"
                result = await load_json_from_url(url, path, True)
                if not result:
                    await refresh.send(f"刷新{i}.json失败,可能是网络问题或api失效")
                    continue
                save_json(result, path)
                logger.info(f"{i}.json文件保存成功")
        elif choose == "别名":
            if (await init_group_card(True)) is False:
                await refresh.finish(f"刷新{choose}失败,可能是网络问题或api失效")
        await refresh.finish(f"刷新{choose}成功")

except (ImportError, ModuleNotFoundError):
    logger.warning("nonebot_adapter_red未安装,跳过red适配器")
