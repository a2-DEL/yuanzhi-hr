"""消息通知插件：系统内消息提醒"""
from app.plugins.base import BasePlugin


class NotificationPlugin(BasePlugin):
    plugin_id = "notification"
    plugin_name = "消息中心"
    version = "1.0.0"
    description = "系统消息通知，包括合同到期提醒、待审批提醒、生日祝福等"
    category = "工具"
    icon = "🔔"

    def on_enable(self) -> bool:
        return True

    def on_disable(self) -> bool:
        return True

    def run(self, action: str, params: dict = None) -> dict:
        if action == "get_notifications":
            return {
                "success": True,
                "notifications": [
                    {"type": "warning", "title": "合同到期提醒", "content": "有3份劳动合同将在90天内到期", "time": "2026-10-05"},
                    {"type": "info", "title": "待审批", "content": "有2条请假申请待审批", "time": "2026-10-05"},
                    {"type": "success", "title": "新员工入职", "content": "陈思 今天入职市场部", "time": "2026-10-05"},
                ]
            }
        elif action == "send_birthday_wish":
            return {"success": True, "message": "生日祝福已发送（示例）"}
        return {"success": False, "error": f"未知操作: {action}"}
