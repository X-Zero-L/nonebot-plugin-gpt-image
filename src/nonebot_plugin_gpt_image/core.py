from nonebot import logger
from openai import AsyncOpenAI
from openai.types.images_response import ImagesResponse

from .config import plugin_config
from .model import (
    ImageQuality,
    ImageSize,
    UserInfo,
)

# 创建OpenAI客户端
client = AsyncOpenAI(api_key=plugin_config.gpt_image_openai_api_key, base_url=plugin_config.gpt_image_base_url)


async def generate_image(
    prompt: str,
    model: str = "gpt-image-1",
    size: ImageSize = ImageSize.SQUARE,
    quality: ImageQuality = ImageQuality.AUTO,
    n: int = 1,
    user_info: UserInfo | None = None,
) -> ImagesResponse:
    """
    使用OpenAI API生成图像
    Args:
        prompt: 图像提示
        model: 模型名称
        size: 图像尺寸
        quality: 图像质量
        n: 生成数量
        response_format: 响应格式
        user_info: 用户信息
    Returns:
        ImagesResponse: OpenAI响应对象
    """
    response = await client.images.generate(
        model=model,
        prompt=prompt,
        n=n,
        size=size.value,
        quality=quality.value,
        user=user_info.get_unique_id() if user_info else None,
    )

    logger.info(f"图像生成成功: {response}")
    return response


async def edit_image(
    images: list[bytes],
    prompt: str,
    model: str = "gpt-image-1",
    size: ImageSize = ImageSize.SQUARE,
    quality: ImageQuality = ImageQuality.AUTO,
    n: int = 1,
    user_info: UserInfo | None = None,
) -> ImagesResponse:
    """
    使用OpenAI API编辑图像
    Args:
        images: 图像二进制数据列表
        prompt: 图像编辑提示
        model: 模型名称
        size: 图像尺寸
        quality: 图像质量
        n: 生成数量
        user_info: 用户信息
    Returns:
        ImagesResponse: OpenAI响应对象
    """
    response = await client.images.edit(
        model=model,
        image=images,
        prompt=prompt,
        n=n,
        size=size.value,
        quality=quality.value,
        user=user_info.get_unique_id() if user_info else None,
    )
    if response.data is None:
        raise ValueError(f"未能获取图像数据，模型返回：{response}")
    logger.info(f"图像编辑成功: {response}")
    return response
