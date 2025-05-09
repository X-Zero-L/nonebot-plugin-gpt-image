<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-gpt-image ✨

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/X-Zero-L/nonebot-plugin-gpt-image.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-gpt-image">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-gpt-image.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</a>
</div>

> [!IMPORTANT] > **收藏项目** ～ ⭐️

<img width="100%" src="https://starify.komoridevs.icu/api/starify?owner=X-Zero-L&repo=nonebot-plugin-gpt-image" alt="starify" />

## 📖 介绍

基于 OpenAI 图像生成 API 的 NoneBot2 插件，支持使用自然语言提示生成/编辑图像。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-gpt-image --upgrade

使用 **pypi** 源安装

    nb plugin install nonebot-plugin-gpt-image --upgrade -i "https://pypi.org/simple"

使用**清华源**安装

    nb plugin install nonebot-plugin-gpt-image --upgrade -i "https://pypi.tuna.tsinghua.edu.cn/simple"

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details open>
<summary>uv</summary>

    uv add nonebot-plugin-gpt-image

安装仓库 master 分支

    uv add git+https://github.com/X-Zero-L/nonebot-plugin-gpt-image@master

</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-gpt-image

安装仓库 master 分支

    pdm add git+https://github.com/X-Zero-L/nonebot-plugin-gpt-image@master

</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-gpt-image

安装仓库 master 分支

    poetry add git+https://github.com/X-Zero-L/nonebot-plugin-gpt-image@master

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_gpt_image"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|          配置项          | 必填 |           默认值            |                      说明                       |
| :----------------------: | :--: | :-------------------------: | :---------------------------------------------: |
| gpt_image_openai_api_key |  是  |             ""              |                 OpenAI API 密钥                 |
|  gpt_image_image_model   |  否  |        "gpt-image-1"        |                图像生成模型名称                 |
|      gpt_image_size      |  否  |         "1024x1024"         | 图像尺寸，可选: 1024x1024, 1024x1792, 1792x1024 |
|    gpt_image_quality     |  否  |           "auto"            |     图像质量，可选: auto, high, medium, low     |
|    gpt_image_base_url    |  否  | "https://api.openai.com/v1" |               OpenAI API 基础 URL               |

## 🎉 使用

### 指令表

|              指令               |   权限   | 需要@ |    范围    |         说明          |
| :-----------------------------: | :------: | :---: | :--------: | :-------------------: |
|       /gpt 生图 <提示词>        | 所有用户 |  否   | 私聊和群聊 |  生成指定内容的图像   |
|    /gpt 生图 <提示词> [图片]    | 所有用户 |  否   | 私聊和群聊 | 编辑图片（支持多图）  |
| /gpt 生图 <提示词> -尺寸 <选项> | 所有用户 |  否   | 私聊和群聊 | 指定尺寸生成/编辑图像 |
| /gpt 生图 <提示词> -质量 <选项> | 所有用户 |  否   | 私聊和群聊 | 指定质量生成/编辑图像 |
|          /gpt 画图帮助          | 所有用户 |  否   | 私聊和群聊 |     显示帮助信息      |

**注意**：编辑图片时，可以直接在消息中附带图片，也可以回复含有图片的消息。

### 尺寸选项

- 方形/正方形/square: 1024x1024(默认)
- 竖版/竖图/portrait: 1024x1792
- 横版/横图/landscape: 1792x1024

### 质量选项

- 低/low: 低质量
- 中/medium: 中等质量
- 高/high: 高质量
- 自动/auto: 自动选择(默认)

### 🎨 效果图

![GPT图像生成效果示例](https://images.openai.com/blob/b196df3a-3a43-4457-9922-e9c7a5a46402/quality-hd.png?trim=0,0,0,0&width=2000)
