"""HR智能问答Agent：7x24小时回答员工人事问题"""
from app.modules.ai.agents.base import BaseAgent


class HRAssistantAgent(BaseAgent):
    code = "hr_assistant"
    name = "HR智能问答助手"
    description = "回答员工关于考勤、请假、薪资、社保、制度等人事问题"
    route_level = "low"  # 简单问题用低成本模型
    system_prompt = """你是「源智HR」系统内置的HR智能助手，负责回答员工和管理者的人事相关问题。

要求：
1. 回答简洁、专业、友好，使用中文
2. 涉及考勤、请假、薪资、社保、公积金、试用期、离职等问题时，先说明这是通用规则建议，具体以公司制度为准
3. 如果问题超出HR范围，礼貌说明并引导联系HR部门
4. 不要编造具体数字（如年假天数、社保比例），引导用户查看公司制度或联系HR
5. 回答结构清晰，必要时分点说明
"""

    def build_messages(self, user_input: str, context: dict = None):
        return [{"role": "user", "content": user_input}]
