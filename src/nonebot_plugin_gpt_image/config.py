from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel, Field


class Config(BaseModel):
    """GPT图像生成插件配置"""

    gpt_image_openai_api_key: str = Field("", description="OpenAI API密钥")
    gpt_image_image_model: str = Field("gpt-image-1", description="图像生成模型名称")
    gpt_image_size: str = Field("1024x1024", description="图像尺寸，可选: 1024x1024, 1024x1792, 1792x1024")
    gpt_image_quality: str = Field("auto", description="图像质量，可选: auto, low, medium, high")
    gpt_image_base_url: str = Field("https://api.openai.com/v1", description="OpenAI API基础URL")


# 配置加载
plugin_config: Config = get_plugin_config(Config)
global_config = get_driver().config

# 全局名称
NICKNAME: str = next(iter(global_config.nickname), "Bot")
