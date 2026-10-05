"""插件基类：所有业务插件都继承这个类"""
from abc import ABC, abstractmethod
from typing import Any


class BasePlugin(ABC):
    """插件基类"""

    # 插件元信息（子类必须定义）
    plugin_id: str = ""          # 唯一ID，如 "data_export"
    plugin_name: str = ""        # 显示名称
    version: str = "1.0.0"
    description: str = ""        # 功能描述
    category: str = "工具"       # 分类：工具/AI/业务/集成
    icon: str = "🔌"            # 图标

    @abstractmethod
    def on_enable(self) -> bool:
        """插件启用时调用，返回是否成功"""
        pass

    @abstractmethod
    def on_disable(self) -> bool:
        """插件禁用时调用"""
        pass

    @abstractmethod
    def run(self, action: str, params: dict = None) -> dict:
        """执行插件功能"""
        pass

    def get_info(self) -> dict:
        return {
            "plugin_id": self.plugin_id,
            "plugin_name": self.plugin_name,
            "version": self.version,
            "description": self.description,
            "category": self.category,
            "icon": self.icon,
        }
