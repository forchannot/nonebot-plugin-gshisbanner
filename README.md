<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://ghproxy.com/https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://ghproxy.com/https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-gshisbanner

_✨ 本插件用于在机器人上查询原神历史卡池信息 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/forchannot/nonebot-plugin-gshisbanner.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-gshisbanner">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-gshisbanner.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

本插件用于在机器人上查询原神历史卡池信息

## 💿 安装

<details>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-gshisbanner
</details>

<details>
<summary>pip</summary>

    pip install nonebot-plugin-gshisbanner
打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_gshisbanner"]
</details>

## ⚙️ 配置
```
gshisbanner_forward_length=10
# 单次合并转发消息长度（int）,默认为10
# 越大单次转发内容更多，合并转发的次数更少，越小单单次转发内容更少，但合并转发的次数更多
# 不要设置为>99或者<0的数字或者任意字符串
```

## 🎉 使用
### 指令表
|        指令         |    权限    | 需要@ | 范围 |                             说明                             |
| :-----------------: | :--------: | :---: | :--: | :----------------------------------------------------------: |
| [name]历史卡池(num) |    ALL     |  否   | ALL  | name必填，为角色名字或别名；num选填，为单次合并转发次数，若无则为gshisbanner_forward_length的值 |
| [version]卡池[num]  |    ALL     |  否   | ALL  | version为版本号，如1.3，2.6等，num为1-3，对应上半（中）下半，可不填，如不填则发送该版本全部卡池 |
|  刷新历史卡池/别名  | 管理员以上 |  否   | ALL  |                      刷新历史卡池或别名                      |
### 效果图
<details>
<summary>历史卡池效果图</summary>
<details>
<summary>图1</summary>
<img src="https://cdn.staticaly.com/gh/forchannot/mypicgo@main/20230324/image.4jlu5w0mhko0.jpg" alt="help">
</details>
<details>
<summary>图2</summary>
<img src="https://cdn.staticaly.com/gh/forchannot/mypicgo@main/20230324/image.5v8oqbhsm080.jpg" alt="help">
</details>
<details>
<summary>图3</summary>
<img src="https://cdn.staticaly.com/gh/forchannot/mypicgo@main/20230324/image.mr1g032ci74.jpg" alt="help">
</details>
</details>

<details>
<summary>版本卡池效果图</summary>
<details>
<summary>图1</summary>
<img src="https://cdn.staticaly.com/gh/forchannot/mypicgo@main/20230324/image.16h2b0rhhlcw.jpg" alt="help">
</details>
<details>
<summary>图2</summary>
<img src="https://cdn.staticaly.com/gh/forchannot/mypicgo@main/20230324/image.50oudvw9cdg0.jpg" alt="help">
</details>
<details>
<summary>图3</summary>
<img src="https://cdn.staticaly.com/gh/forchannot/mypicgo@main/20230324/image.63vftfc9ryk0.jpg" alt="help">
</details>
</details>

<details>
<summary>刷新卡池/别名效果图</summary>
<img src="https://cdn.staticaly.com/gh/forchannot/mypicgo@main/20230324/image.5zl59kpx8b00.jpg" alt="help">
</details>
