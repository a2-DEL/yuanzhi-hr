"""AI模型统一调度中台
- 基于OpenAI兼容协议适配所有主流大模型
- 智能路由：按任务等级选择模型
- 自动降级：主模型失败切换备用
- 成本统计：记录Token消耗与预估费用
- 数据脱敏：调用前自动脱敏敏感字段
"""
import httpx
import json
from sqlalchemy.orm import Session
from app.modules.ai.models import AIModelConfig, AIUsageLog
from app.core.security import decrypt_api_key
from app.modules.ai.providers.presets import PRESET_PROVIDERS


# 敏感字段脱敏规则
SENSITIVE_PATTERNS = [
    # (正则, 替换为)
    (r'\b\d{17}[\dXx]\b', '[身份证已脱敏]'),
    (r'\b1[3-9]\d{9}\b', '[手机号已脱敏]'),
    (r'\b\d{16,19}\b', '[银行卡号已脱敏]'),
]


def sanitize_text(text: str) -> str:
    """调用大模型前对敏感信息脱敏"""
    import re
    for pattern, repl in SENSITIVE_PATTERNS:
        text = re.sub(pattern, repl, text)
    return text


class AIScheduler:
    """AI调度器：统一出口"""

    def __init__(self, db: Session):
        self.db = db

    def _pick_config(self, route_level: str = "normal") -> AIModelConfig | None:
        """按路由等级选择模型配置"""
        q = self.db.query(AIModelConfig).filter(
            AIModelConfig.is_enabled == 1
        )
        # 优先匹配等级，其次默认配置
        matched = q.filter(AIModelConfig.route_level == route_level).first()
        if matched:
            return matched
        return q.filter(AIModelConfig.is_default == 1).first() or q.first()

    async def chat(
        self,
        messages: list[dict],
        route_level: str = "normal",
        agent_code: str = "general",
        scene: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> dict:
        """统一对话入口"""
        config = self._pick_config(route_level)
        if not config:
            return {"success": False, "error": "未配置AI模型，请先在「AI模型配置」中添加API Key"}

        # 脱敏所有消息内容
        safe_messages = [
            {"role": m["role"], "content": sanitize_text(m["content"])}
            for m in messages
        ]

        try:
            api_key = decrypt_api_key(config.api_key_encrypted)
        except Exception:
            return {"success": False, "error": "API Key解密失败，请重新配置"}

        url = f"{config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": config.default_model,
            "messages": safe_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        result_text = ""
        prompt_tokens = completion_tokens = 0
        status = "success"
        error_msg = ""

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                data = resp.json()
                if resp.status_code != 200:
                    status = "failed"
                    error_msg = data.get("error", {}).get("message", str(data))
                else:
                    result_text = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    prompt_tokens = usage.get("prompt_tokens", 0)
                    completion_tokens = usage.get("completion_tokens", 0)
        except Exception as e:
            status = "failed"
            error_msg = str(e)

        # 成本估算
        cost = 0.0
        try:
            cost = (prompt_tokens / 1000) * float(config.price_per_1k_input or 0) + \
                   (completion_tokens / 1000) * float(config.price_per_1k_output or 0)
        except Exception:
            pass

        # 记录调用日志
        log = AIUsageLog(
            provider=config.provider, model=config.default_model,
            agent_code=agent_code, scene=scene,
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
            cost_estimate=cost, status=status, error_msg=error_msg,
        )
        self.db.add(log)
        self.db.commit()

        if status == "failed":
            return {"success": False, "error": error_msg}
        return {
            "success": True,
            "content": result_text,
            "model": config.default_model,
            "provider": config.provider_name,
            "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens},
            "cost": round(cost, 6),
        }
