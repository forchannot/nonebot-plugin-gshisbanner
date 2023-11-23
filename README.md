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
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
<br />
<a href="https://onebot.dev/">
    <img src="https://img.shields.io/badge/OneBot-v11-black?style=social&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="onebot">
</a>
</div>

## 📖 介绍

本插件用于在机器人上查询原神历史卡池信息（当前仅适用于qq）

1.0.0版本开始同时支持了onebot v11协议和red协议，欢迎尝鲜

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
gshisbanner_forward_length: int
# 单次合并转发消息长度（int）,默认为10
# 仅为角色/武器卡池转发内容长度，不包括版本卡池
# 越大单次转发内容更多，合并转发的次数更少，越小单单次转发内容更少，但合并转发的次数更多
# 不要设置为>99或者<0的数字或者任意字符串

gshisbanner_json_url: str
# 历史卡池json列表下载位置
# 可选值
·· 1."banners.52v6.com/data" 
     #默认，推荐
·· 2."genshin-gacha-banners.vercel.app/data" 
     #vercel代理，国内可能无法直连
·· 3."genshin-gacha-banners.52v6.com/data" 
     #cloudfare代理，可能会被墙
·· 4."mirror.ghproxy.com/https://raw.githubusercontent.com/KeyPJ/FetchData/main/data/gacha" 
     ##ghproxy代理的raw文件，大多数情况可用，不过不稳定
     ##前面的"ghproxy.com/"可以不写(如果你是国外机),或者换成你自建的github加速服务均可(需要支持https)
·· 5."jsd.cdn.zzko.cn/gh/KeyPJ/FetchData@main/data/gacha"
     ##jsdelivr代理的文件，大多数情况可用，推荐
```
**也可以将上述4和5中的`KeyPJ`更改为`forchannot`，或者自己尝试复制json文件到数据目录`{bot_dir}/data/genshin_history`**

## 🎉 使用
### 指令表
#### 用前提示，本插件采用on_keyword，不需要带你设置的command_start，当然，如果你非要带，本插件做了一定的处理
|        指令        |  权限   | 需要@ | 范围  |                                说明                                |
|:----------------:|:-----:|:---:|:---:|:----------------------------------------------------------------:|
| [name]历史卡池(num)  |  ALL  |  否  | ALL | name必填，为角色名字或别名；num选填，为单次合并转发次数，若无则为gshisbanner_forward_length的值 |
| [version]卡池[num] |  ALL  |  否  | ALL |    version为版本号，如1.3，2.6等，num为1-3，对应上半（中）下半，可不填，如不填则发送该版本全部卡池     |
|  刷新(更新)历史卡池/别名   | 管理员以上 |  否  | ALL |                            刷新历史卡池或别名                             |
### 效果图
<details>
<summary>历史卡池效果图</summary>
<details>
<summary>图1</summary>
<img src="https://jsd.cdn.zzko.cn/gh/forchannot/mypicgo@main/20230324/image.4jlu5w0mhko0.jpg" alt="help">
</details>
<details>
<summary>图2</summary>
<img src="https://jsd.cdn.zzko.cn/gh/forchannot/mypicgo@main/20230324/image.5v8oqbhsm080.jpg" alt="help">
</details>
<details>
<summary>图3</summary>
<img src="https://jsd.cdn.zzko.cn/gh/forchannot/mypicgo@main/20230324/image.mr1g032ci74.jpg" alt="help">
</details>
</details>

<details>
<summary>版本卡池效果图</summary>
<details>
<summary>图1</summary>
<img src="https://jsd.cdn.zzko.cn/gh/forchannot/mypicgo@main/20230324/image.16h2b0rhhlcw.jpg" alt="help">
</details>
<details>
<summary>图2</summary>
<img src="https://jsd.cdn.zzko.cn/gh/forchannot/mypicgo@main/20230324/image.50oudvw9cdg0.jpg" alt="help">
</details>
<details>
<summary>图3</summary>
<img src="https://jsd.cdn.zzko.cn/gh/forchannot/mypicgo@main/20230324/image.63vftfc9ryk0.jpg" alt="help">
</details>
</details>

<details>
<summary>刷新卡池/别名效果图</summary>
<img src="https://jsd.cdn.zzko.cn/gh/forchannot/mypicgo@main/20230324/image.5zl59kpx8b00.jpg" alt="help">
</details>


### 鸣谢

[genshin-gacha-banners](https://github.com/KeyPJ/genshin-gacha-banners) #历史up卡池来源
