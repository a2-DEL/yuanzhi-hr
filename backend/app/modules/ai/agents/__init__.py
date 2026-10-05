"""Agent注册中心"""
from .base import BaseAgent, AgentResult
from .hr_assistant import HRAssistantAgent
from .resume_parser import ResumeParserAgent
from .salary_assistant import SalaryAssistantAgent
from .team_agents import TEAM_AGENTS, TEAM_AGENTS_DEF

# 内置基础Agent
AGENT_REGISTRY: dict[str, BaseAgent] = {
    HRAssistantAgent.code: HRAssistantAgent(),
    ResumeParserAgent.code: ResumeParserAgent(),
    SalaryAssistantAgent.code: SalaryAssistantAgent(),
}

# 注册所有团队Agent
AGENT_REGISTRY.update(TEAM_AGENTS)


def list_agents() -> list[dict]:
    """列出所有可用Agent"""
    return [
        {"code": a.code, "name": a.name, "description": a.description, "route_level": a.route_level}
        for a in AGENT_REGISTRY.values()
    ]


def get_agent(code: str) -> BaseAgent | None:
    return AGENT_REGISTRY.get(code)
