"""插件注册表：自动发现、注册、管理插件"""
import importlib
import pkgutil
from app.plugins.base import BasePlugin


# 已注册插件实例
_plugin_registry: dict[str, BasePlugin] = {}
# 插件启用状态（从配置/数据库读取，这里先用内存）
_enabled_plugins: set[str] = set()


def discover_plugins():
    """自动发现builtin目录下的所有插件"""
    _plugin_registry.clear()
    _enabled_plugins.clear()

    # 遍历builtin目录
    package = "app.plugins.builtin"
    for importer, modname, ispkg in pkgutil.iter_modules([package.replace(".", "/")]):
        try:
            mod = importlib.import_module(f"{package}.{modname}")
            # 查找模块中BasePlugin的子类
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if (isinstance(attr, type) and issubclass(attr, BasePlugin)
                        and attr is not BasePlugin and attr.plugin_id):
                    instance = attr()
                    _plugin_registry[instance.plugin_id] = instance
        except Exception as e:
            print(f"[插件] 加载 {modname} 失败: {e}")

    print(f"[插件] 已发现 {len(_plugin_registry)} 个插件: {list(_plugin_registry.keys())}")


def list_plugins() -> list[dict]:
    """列出所有插件及状态"""
    result = []
    for pid, plugin in _plugin_registry.items():
        info = plugin.get_info()
        info["enabled"] = pid in _enabled_plugins
        result.append(info)
    return result


def enable_plugin(plugin_id: str) -> bool:
    """启用插件"""
    plugin = _plugin_registry.get(plugin_id)
    if not plugin:
        return False
    if plugin.on_enable():
        _enabled_plugins.add(plugin_id)
        return True
    return False


def disable_plugin(plugin_id: str) -> bool:
    """禁用插件"""
    plugin = _plugin_registry.get(plugin_id)
    if not plugin:
        return False
    if plugin.on_disable():
        _enabled_plugins.discard(plugin_id)
        return True
    return False


def run_plugin(plugin_id: str, action: str, params: dict = None) -> dict:
    """执行插件"""
    plugin = _plugin_registry.get(plugin_id)
    if not plugin:
        return {"success": False, "error": "插件不存在"}
    if plugin_id not in _enabled_plugins:
        return {"success": False, "error": "插件未启用"}
    return plugin.run(action, params or {})
