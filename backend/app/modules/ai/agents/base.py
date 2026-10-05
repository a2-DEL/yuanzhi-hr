"""Agent基类：所有HR专业Agent的统一接口"""
from abc import ABC, abstractmethod
from pydantic import BaseModel
from app.modules.ai.scheduler import AIScheduler


class AgentResult(BaseModel):
    success: bool
    content: str
    agent_code: str
    agent_name: str
    model: str = ""
    cost: float = 0.0
    extra: dict = {}


class BaseAgent(ABC):
    """所有Agent的抽象基类"""
    code: str = ""
    name: str = ""
    description: str = ""
    system_prompt: str = ""
    route_level: str = "normal"  # high/normal/low

    @abstractmethod
    def build_messages(self, user_input: str, context: dict = None) -> list[dict]:
        """构建消息列表"""
        pass

    async def run(self, scheduler: AIScheduler, user_input: str, context: dict = None) -> AgentResult:
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.build_messages(user_input, context or {}))
        result = await scheduler.chat(
            messages=messages,
            route_level=self.route_level,
            agent_code=self.code,
            scene=self.name,
        )
        if not result["success"]:
            return AgentResult(
                success=False, content=result["error"],
                agent_code=self.code, agent_name=self.name,
            )
        return AgentResult(
            success=True, content=result["content"],
            agent_code=self.code, agent_name=self.name,
            model=result.get("model", ""), cost=result.get("cost", 0),
        )
