from enum import Enum

from pydantic import BaseModel


class ImageSize(str, Enum):
    """图像尺寸选项"""

    SQUARE = "1024x1024"
    PORTRAIT = "1024x1792"
    LANDSCAPE = "1792x1024"


class ImageQuality(str, Enum):
    """图像质量选项"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    AUTO = "auto"


class ImageStyle(str, Enum):
    """图像风格选项"""

    NATURAL = "natural"
    VIVID = "vivid"


class ImageMode(str, Enum):
    """图像操作模式"""

    GENERATE = "generate"  # 生成模式
    EDIT = "edit"  # 编辑模式


class UserInfo(BaseModel):
    """用户信息"""

    user_id: str
    platform: str

    def get_unique_id(self) -> str:
        """获取用户唯一标识"""
        return f"{self.platform}_{self.user_id}"
