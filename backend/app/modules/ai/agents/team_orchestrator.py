"""
多Agent团队调度器
HR总监总控Agent：理解需求 → 选择团队 → 调用对应Agent执行
"""
from app.modules.ai.agents.base import BaseAgent, AgentResult
from app.modules.ai.scheduler import AIScheduler
from app.modules.ai.agents.team_agents import TEAM_AGENTS_DEF, TEAM_AGENTS


# 团队定义（用于前端展示）
TEAMS = {
    "planning": {
        "name": "人力资源规划团队", "icon": "📊",
        "description": "组织架构设计、编制规划、人力成本预算、岗位说明书、制度体系搭建",
    },
    "recruitment": {
        "name": "招聘与配置团队", "icon": "🎯",
        "description": "招聘需求分析、渠道策略、简历筛选、面试评估、录用决策",
    },
    "training": {
        "name": "培训与开发团队", "icon": "📚",
        "description": "培训需求调研、课程设计、人才梯队建设、职业发展规划",
    },
    "performance": {
        "name": "绩效管理团队", "icon": "📈",
        "description": "KPI/OKR设计、考核周期组织、绩效面谈、结果应用",
    },
    "compensation": {
        "name": "薪酬福利团队", "icon": "💰",
        "description": "薪资体系设计、社保公积金、个税核算、福利规划、人力成本分析",
    },
    "relation": {
        "name": "员工关系团队", "icon": "🤝",
        "description": "劳动合同、入转调离、员工关怀、劳动合规、离职分析",
    },
}


class HRDirectorAgent(BaseAgent):
    """HR总监：先判断该派给哪个团队，再实际调用对应Agent执行"""
    code = "hr_director"
    name = "HR总监总控"
    description = "理解HR需求，自动调度专业团队执行"
    route_level = "high"

    system_prompt = """你是「源智HR」的HR总监。根据用户需求，判断应该派给哪个专业团队的哪个Agent。

可选团队：
- planning（人力规划）：组织架构/编制/JD/制度
- recruitment（招聘）：需求/简历/面试/Offer
- training（培训）：需求分析/课程/人才梯队
- performance（绩效）：KPI/面谈/结果分析
- compensation（薪酬）：薪资体系/核算/成本
- relation（员工关系）：合同/入职/合规/离职

你只输出一个JSON，不要多余解释：
{"team": "团队code", "agent": "Agent code", "reason": "简短理由"}

例如：{"team": "recruitment", "agent": "resume_screener", "reason": "用户在问简历筛选"}"""

    def build_messages(self, user_input: str, context: dict = None) -> list[dict]:
        return [{"role": "user", "content": f"用户需求：{user_input}\n请判断调度哪个团队哪个Agent，输出JSON。"}]


class TeamOrchestrator:
    """团队调度器：总控判断 → 实际执行"""

    def __init__(self, scheduler: AIScheduler):
        self.scheduler = scheduler
        self.director = HRDirectorAgent()

    async def dispatch_and_run(self, user_input: str) -> dict:
        """第一步：HR总监判断路由；第二步：调用对应Agent实际执行"""
        import json

        # 第一步：总控判断路由
        director_result = await self.director.run(self.scheduler, user_input)

        routed_team = None
        routed_agent = None
        route_reason = ""

        if director_result.success:
            try:
                # 提取JSON
                text = director_result.content.strip()
                # 找到第一个{到最后一个}
                start = text.find("{")
                end = text.rfind("}")
                if start >= 0 and end > start:
                    data = json.loads(text[start:end+1])
                    routed_team = data.get("team")
                    routed_agent = data.get("agent")
                    route_reason = data.get("reason", "")
            except Exception:
                pass

        # 第二步：调用对应Agent执行
        execution = None
        if routed_agent and routed_agent in TEAM_AGENTS:
            agent = TEAM_AGENTS[routed_agent]
            exec_result = await agent.run(self.scheduler, user_input)
            execution = {
                "agent_code": exec_result.agent_code,
                "agent_name": exec_result.agent_name,
                "team": agent.team,
                "content": exec_result.content if exec_result.success else f"执行失败：{exec_result.content}",
                "model": exec_result.model,
                "cost": exec_result.cost,
            }
        else:
            # 路由失败，降级为通用问答
            execution = {
                "agent_code": "fallback",
                "agent_name": "通用HR助手",
                "team": "unknown",
                "content": director_result.content,
            }

        return {
            "director_analysis": director_result.content,
            "routed_team": routed_team,
            "routed_agent": routed_agent,
            "route_reason": route_reason,
            "execution": execution,
        }

    def get_team_definitions(self) -> dict:
        """返回团队+主管+Agent完整定义"""
        from app.modules.ai.agents.team_agents import TEAM_LEADS, TEAM_META
        result = {}
        for team_key, meta in TEAM_META.items():
            agents = []
            for agent_code, agent_def in TEAM_AGENTS_DEF.items():
                if agent_def["team"] == team_key:
                    agents.append({
                        "code": agent_code,
                        "name": agent_def["name"],
                        "desc": agent_def["desc"],
                    })
            lead = TEAM_LEADS.get(team_key, {})
            result[team_key] = {
                "key": team_key,
                "name": meta["name"],
                "icon": meta["icon"],
                "color": meta["color"],
                "lead": lead,
                "agent_count": len(agents),
                "agents": agents,
            }
        return result
