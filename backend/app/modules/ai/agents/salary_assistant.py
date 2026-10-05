"""薪资核算辅助Agent：生成薪资说明、个税测算、人力成本分析"""
from app.modules.ai.agents.base import BaseAgent


class SalaryAssistantAgent(BaseAgent):
    code = "salary_assistant"
    name = "薪资核算辅助Agent"
    description = "辅助HR进行薪资说明生成、个税测算、人力成本分析"
    route_level = "normal"
    system_prompt = """你是专业的薪酬福利专家，负责辅助HR处理薪资相关工作。

能力范围：
1. 根据员工情况生成薪资构成说明（基本工资、绩效、补贴、扣款）
2. 解释个税计算逻辑（提示用户这是说明，具体以税务部门为准）
3. 分析部门人力成本结构
4. 生成调薪建议报告

要求：
- 数字计算准确，不确定时明确说明"需以实际财务数据为准"
- 涉及法律政策时，提示"具体以当地最新政策为准"
- 输出结构化，条理清晰
"""

    def build_messages(self, user_input: str, context: dict = None):
        return [{"role": "user", "content": user_input}]
