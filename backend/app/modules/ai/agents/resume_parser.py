"""简历解析与匹配Agent：自动解析简历、人岗匹配打分"""
from app.modules.ai.agents.base import BaseAgent


class ResumeParserAgent(BaseAgent):
    code = "resume_parser"
    name = "简历解析与匹配Agent"
    description = "自动解析简历内容，提取关键信息，按岗位要求打分推荐"
    route_level = "high"  # 简历分析用高精度模型
    system_prompt = """你是专业的招聘筛选专家，负责解析候选人简历并与岗位要求匹配。

请按以下JSON格式输出（不要输出其他内容）：
{
  "name": "姓名",
  "education": "最高学历",
  "school": "毕业院校",
  "major": "专业",
  "work_years": 数字,
  "current_position": "当前职位",
  "core_skills": ["技能1", "技能2"],
  "match_score": 0-100的整数,
  "strengths": ["优势1", "优势2"],
  "concerns": ["疑虑1", "疑虑2"],
  "recommendation": "strong_recommend/recommend/hold/reject"
}

打分原则：
- 学历、工作年限、核心技能与岗位匹配度是主要评分依据
- 稳定性（跳槽频率）作为扣分项
- 输出必须是合法JSON，不要有多余文字
"""

    def build_messages(self, user_input: str, context: dict = None):
        job_requirement = context.get("job_requirement", "未提供岗位要求")
        return [
            {"role": "system", "content": f"岗位要求：{job_requirement}"},
            {"role": "user", "content": f"请解析以下简历并输出JSON：\n\n{user_input}"},
        ]
