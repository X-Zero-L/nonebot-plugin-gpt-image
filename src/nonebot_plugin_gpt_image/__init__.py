from nonebot import logger, require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_waiter")
require("nonebot_plugin_uninfo")
require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")

import base64

import aiohttp

from .config import Config, plugin_config

__plugin_meta__ = PluginMetadata(
    name="GPT图像生成",
    description="使用OpenAI图像生成API创建图像",
    usage="发送 /gpt生图 <提示词> 生成图像，传入图片/回复图片则进入编辑模式",
    type="application",
    homepage="https://github.com/X-Zero-L/nonebot-plugin-gpt-image",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna", "nonebot_plugin_uninfo"),
    extra={"author": "X-Zero-L <zeroeeau@gmail.com>"},
)


from arclet.alconna import Alconna, AllParam, Args, Option
from nonebot.adapters import Bot, Event
from nonebot.exception import FinishedException
from nonebot_plugin_alconna import Match, MsgId, UniMessage, on_alconna
from nonebot_plugin_alconna.builtins.extensions import ReplyRecordExtension
from nonebot_plugin_alconna.uniseg import Image as AlconnaImage
from nonebot_plugin_alconna.uniseg import Text
from nonebot_plugin_uninfo import Uninfo
from openai.types.images_response import ImagesResponse

from .core import edit_image, generate_image
from .model import ImageMode, ImageQuality, ImageSize, UserInfo

# 图像生成命令
image_cmd = on_alconna(
    Alconna(
        "/gpt生图",
        Args["prompt", str],
        Args["image?", AllParam],
        Option("-尺寸|-s", Args["size", str], help_text="图像尺寸: 方形/竖版/横版"),
        Option("-质量|-q", Args["quality", str], help_text="图像质量: 低/中/高/自动"),
    ),
    use_cmd_start=True,
    block=True,
    aliases={"/gpt画图", "/gpt生成图像", "/gpt_image", "/gi"},
    extensions=[ReplyRecordExtension()],
)

# 帮助命令
help_cmd = on_alconna(
    Alconna("/gpt画图帮助"),
    use_cmd_start=True,
    block=True,
)


def parse_size(size_str: str) -> ImageSize:
    """解析尺寸参数"""
    size_map = {
        "方形": ImageSize.SQUARE,
        "正方形": ImageSize.SQUARE,
        "square": ImageSize.SQUARE,
        "竖版": ImageSize.PORTRAIT,
        "竖图": ImageSize.PORTRAIT,
        "portrait": ImageSize.PORTRAIT,
        "横版": ImageSize.LANDSCAPE,
        "横图": ImageSize.LANDSCAPE,
        "landscape": ImageSize.LANDSCAPE,
        "自动": ImageSize.AUTO,
        "auto": ImageSize.AUTO,
    }
    return size_map.get(size_str.lower(), ImageSize.AUTO)


def parse_quality(quality_str: str) -> ImageQuality:
    """解析质量参数"""
    quality_map = {
        "低": ImageQuality.LOW,
        "中": ImageQuality.MEDIUM,
        "高": ImageQuality.HIGH,
        "自动": ImageQuality.AUTO,
        "low": ImageQuality.LOW,
        "medium": ImageQuality.MEDIUM,
        "high": ImageQuality.HIGH,
        "auto": ImageQuality.AUTO,
    }
    return quality_map.get(quality_str.lower(), ImageQuality.AUTO)


async def get_image_data_from_url(url: str) -> bytes | None:
    """从URL获取图片数据"""
    try:
        logger.info(f"获取图像数据: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    logger.error(f"无法获取图片数据: {resp.status}")
                    return None
                return await resp.read()
    except Exception as e:
        logger.error(f"获取图像数据失败: {e}")
        return None


async def to_image_data(image: AlconnaImage) -> bytes | None:
    """从AlconnaImage获取图片数据"""
    try:
        if image.raw is not None:
            return image.raw

        if image.url is not None:
            return await get_image_data_from_url(image.url)

        return None
    except Exception as e:
        logger.error(f"获取图像数据失败: {e}")
        return None


def responser2images(response: ImagesResponse) -> list[AlconnaImage]:
    """将API响应转换为Alconna图像列表"""
    images = []
    for data in response.data:
        if data.b64_json:
            images.append(AlconnaImage(raw=base64.b64decode(data.b64_json)))
        elif data.url:
            images.append(AlconnaImage(url=data.url))
    return images


async def collect_images(event: Event, ext: ReplyRecordExtension, msg_id: MsgId, bot: Bot) -> list[bytes]:
    """收集所有图片数据，包括回复中的图片"""
    image_list: list[bytes] = []

    # 处理回复中的图片
    reply = ext.get_reply(msg_id)
    if reply:
        try:
            uni_reply = await UniMessage.generate(message=reply.msg, event=event, bot=bot)
            for segment in uni_reply:
                if isinstance(segment, AlconnaImage):
                    img_bytes = await to_image_data(segment)
                    if img_bytes:
                        image_list.append(img_bytes)
        except Exception as e:
            logger.error(f"处理回复消息中的图片出错: {e}")

    # 处理当前消息中的图片
    try:
        message = await UniMessage.generate(event=event, bot=bot)
        for segment in message:
            if isinstance(segment, AlconnaImage):
                img_bytes = await to_image_data(segment)
                if img_bytes:
                    image_list.append(img_bytes)
    except Exception as e:
        logger.error(f"处理消息中图片出错: {e}")

    return image_list


@image_cmd.handle()
async def handle_image(
    bot: Bot,
    event: Event,
    uninfo: Uninfo,
    prompt: Match[str],
    ext: ReplyRecordExtension,
    msg_id: MsgId,
    size: Match[str] = None,
    quality: Match[str] = None,
):
    """处理图像生成请求"""
    try:
        user_info = UserInfo(user_id=uninfo.user.id, platform=bot.adapter.get_name())
        prompt_text = prompt.result
        image_list = await collect_images(event, ext, msg_id, bot)
        image_mode = ImageMode.EDIT if image_list else ImageMode.GENERATE

        if image_mode == ImageMode.EDIT:
            await UniMessage(f"正在编辑 {len(image_list)} 张图像，请稍候...").reply(id=msg_id).send()
        else:
            await UniMessage("正在生成图像，请稍候...").reply(id=msg_id).send()

        img_size = ImageSize.SQUARE
        img_quality = ImageQuality.AUTO

        if size and size.available:
            img_size = parse_size(size.result)

        if quality and quality.available:
            img_quality = parse_quality(quality.result)

        all_images = []

        if image_mode == ImageMode.EDIT and image_list:
            try:
                response = await edit_image(
                    images=image_list,
                    prompt=prompt_text,
                    model=plugin_config.gpt_image_image_model,
                    size=img_size,
                    quality=img_quality,
                    user_info=user_info,
                )

                if response and response.data:
                    all_images.extend(responser2images(response))

                mode_text = "已编辑图像"
            except Exception as e:
                logger.error(f"编辑图片失败: {e}")
                await image_cmd.finish(UniMessage(f"编辑图片失败: {e!s}").reply(id=msg_id))
        else:
            response = await generate_image(
                prompt=prompt_text,
                model=plugin_config.gpt_image_image_model,
                size=img_size,
                quality=img_quality,
                user_info=user_info,
            )

            if response and response.data:
                all_images.extend(responser2images(response))

            mode_text = "已生成图像"

        if all_images:
            await image_cmd.finish(UniMessage([Text(mode_text), *all_images]).reply(id=msg_id))
        else:
            await image_cmd.finish(UniMessage("操作失败: 未能获取图像数据").reply(id=msg_id))

    except FinishedException:
        pass
    except ValueError as e:
        await image_cmd.finish(UniMessage(f"操作失败: {e!s}").reply(id=msg_id))
    except Exception as e:
        logger.error(f"操作出错: {e}")
        await image_cmd.finish(UniMessage(f"操作出错: {e!s}").reply(id=msg_id))


@help_cmd.handle()
async def handle_help():
    """处理帮助请求"""
    help_text = """
GPT图像生成插件使用帮助:

基本命令:
/gpt画图 <提示词> - 使用提供的提示词生成图像
/gpt画图 <提示词> [图片] - 根据提示词编辑图片

参数选项:
-尺寸 [方形/竖版/横版] - 设置生成图像的尺寸, 默认方形
-质量 [低/中/高/自动] - 设置生成图像的质量, 默认自动

例如:
/gpt画图 一只可爱的猫咪 -尺寸 方形 -质量 高
/gpt画图 添加一顶帽子 [图片] -质量 高

其他命令:
/gpt画图帮助 - 显示此帮助信息
"""

    await help_cmd.finish(UniMessage(help_text))
