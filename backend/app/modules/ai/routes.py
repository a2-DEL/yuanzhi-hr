"""AI模型配置与Agent调用路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.core.security import encrypt_api_key
from app.modules.ai.models import AIModelConfig, AIUsageLog
from app.modules.ai.providers.presets import PRESET_PROVIDERS
from app.modules.ai.scheduler import AIScheduler
from app.modules.ai.agents import list_agents, get_agent

router = APIRouter(prefix="/api/ai", tags=["AI能力中台"])


# ===== 预置厂商列表 =====
@router.get("/providers/presets", summary="获取预置厂商列表")
def presets(_=Depends(get_current_user)):
    return success(PRESET_PROVIDERS)


# ===== 智能识别：根据API Key/地址自动识别厂商 =====
class DetectIn(BaseModel):
    api_key: str
    base_url: str = ""

@router.post("/detect", summary="智能识别API Key对应的厂商")
def detect_provider(body: DetectIn, _=Depends(get_current_user)):
    key = body.api_key.strip()
    url = body.base_url.strip().lower()
    candidates = []

    # 规则1：根据base_url识别（最可靠）
    if "deepseek" in url:
        candidates.append("deepseek")
    if "openai.com" in url:
        candidates.append("openai")
    if "volces" in url or "ark.cn" in url:
        candidates.append("doubao")
    if "aliyun" in url or "dashscope" in url:
        candidates.append("qwen")
    if "bigmodel" in url or "zhipu" in url:
        candidates.append("zhipu")
    if "moonshot" in url:
        candidates.append("moonshot")

    # 规则2：根据Key格式特征识别
    if not candidates:
        # 智谱Key格式：xxxxxx.xxxxxx（带点）
        if "." in key and not key.startswith("sk-"):
            candidates.append("zhipu")
        # 豆包Key通常是UUID格式
        elif len(key) == 36 and key.count("-") == 4:
            candidates.append("doubao")
        # 其他sk-开头的，列出所有可能
        elif key.startswith("sk-"):
            candidates = ["deepseek", "openai", "qwen", "moonshot"]

    # 如果还是识别不出，返回全部候选
    if not candidates:
        candidates = list(PRESET_PROVIDERS.keys())

    # 组装候选信息
    result = []
    for c in candidates:
        p = PRESET_PROVIDERS.get(c, {})
        result.append({
            "provider": c,
            "provider_name": p.get("provider_name", c),
            "base_url": p.get("base_url", ""),
            "default_model": p.get("default_model", ""),
        })

    detected = result[0] if result else None
    return success({"detected": detected, "candidates": result})


# ===== 模型配置CRUD =====
@router.get("/models", summary="模型配置列表")
def model_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    configs = db.query(AIModelConfig).order_by(AIModelConfig.id.desc()).all()
    return success([{
        "id": c.id, "provider": c.provider, "provider_name": c.provider_name,
        "base_url": c.base_url, "default_model": c.default_model,
        "route_level": c.route_level, "is_enabled": c.is_enabled,
        "is_default": c.is_default,
        "price_per_1k_input": float(c.price_per_1k_input or 0),
        "price_per_1k_output": float(c.price_per_1k_output or 0),
        # 不返回api_key
    } for c in configs])


class ModelConfigIn(BaseModel):
    provider: str
    provider_name: str = None
    base_url: str
    api_key: str
    default_model: str
    route_level: str = "normal"
    is_enabled: int = 1
    is_default: int = 0
    price_per_1k_input: float = 0
    price_per_1k_output: float = 0


@router.post("/models", summary="新增模型配置")
def add_model(body: ModelConfigIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    preset = PRESET_PROVIDERS.get(body.provider, {})
    c = AIModelConfig(
        provider=body.provider,
        provider_name=body.provider_name or preset.get("provider_name", body.provider),
        base_url=body.base_url,
        api_key_encrypted=encrypt_api_key(body.api_key),
        default_model=body.default_model or preset.get("default_model"),
        route_level=body.route_level,
        is_enabled=body.is_enabled,
        is_default=body.is_default,
        price_per_1k_input=body.price_per_1k_input,
        price_per_1k_output=body.price_per_1k_output,
    )
    db.add(c); db.commit()
    return success(message="模型配置已保存")


@router.delete("/models/{config_id}", summary="删除模型配置")
def del_model(config_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = db.query(AIModelConfig).get(config_id)
    if c:
        db.delete(c); db.commit()
    return success(msg="已删除")


# ===== 测试连接 =====
import httpx
class TestConnectionIn(BaseModel):
    base_url: str
    api_key: str
    default_model: str

@router.post("/test", summary="测试模型连接是否可用")
async def test_connection(body: TestConnectionIn, _=Depends(get_current_user)):
    url = f"{body.base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {body.api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": body.default_model,
        "messages": [{"role": "user", "content": "你好，请回复'连接成功'四个字"}],
        "max_tokens": 20,
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            data = resp.json()
            if resp.status_code == 200:
                content = data["choices"][0]["message"]["content"]
                return success({"success": True, "reply": content, "model": body.default_model})
            else:
                err = data.get("error", {}).get("message", str(data))
                return success({"success": False, "error": err})
    except Exception as e:
        return success({"success": False, "error": f"连接失败：{str(e)}"})


# ===== Agent列表与调用 =====
@router.get("/agents", summary="可用Agent列表")
def agent_list(_=Depends(get_current_user)):
    return success(list_agents())


class AgentCallIn(BaseModel):
    agent_code: str
    input: str
    context: dict = {}


@router.post("/agents/call", summary="调用Agent")
async def call_agent(body: AgentCallIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    agent = get_agent(body.agent_code)
    if not agent:
        raise AppException(message="Agent不存在")
    scheduler = AIScheduler(db)
    result = await agent.run(scheduler, body.input, body.context)
    if not result.success:
        raise AppException(message=result.content)
    return success({
        "content": result.content,
        "agent": {"code": result.agent_code, "name": result.agent_name},
        "model": result.model,
        "cost": result.cost,
    })


# ===== 调用统计 =====
@router.get("/usage/stats", summary="AI调用统计")
def usage_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    logs = db.query(AIUsageLog).all()
    total_calls = len(logs)
    total_tokens = sum(l.prompt_tokens + l.completion_tokens for l in logs)
    total_cost = sum(float(l.cost_estimate or 0) for l in logs)
    success_calls = sum(1 for l in logs if l.status == "success")
    return success({
        "total_calls": total_calls,
        "success_calls": success_calls,
        "total_tokens": total_tokens,
        "total_cost": round(total_cost, 4),
    })


# ===== 多Agent团队 =====
from app.modules.ai.agents.team_orchestrator import TeamOrchestrator

@router.get("/teams", summary="获取所有Agent团队（含执行Agent列表）")
def get_teams(_=Depends(get_current_user)):
    orch = TeamOrchestrator(AIScheduler)
    return success(orch.get_team_definitions())


class DirectorDispatchIn(BaseModel):
    user_input: str

@router.post("/teams/dispatch", summary="HR总监总控调度并实际执行")
async def director_dispatch(body: DirectorDispatchIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    scheduler = AIScheduler(db)
    orch = TeamOrchestrator(scheduler)
    result = await orch.dispatch_and_run(body.user_input)
    return success(result)


# ===== 合规引擎 =====
@router.get("/compliance/rules", summary="获取合规规则库")
def compliance_rules(_=Depends(get_current_user)):
    from app.modules.ai.compliance import get_rules
    return success(get_rules())


class ComplianceCheckIn(BaseModel):
    category: str
    data: dict = {}

@router.post("/compliance/check", summary="合规检查")
def compliance_check(body: ComplianceCheckIn, _=Depends(get_current_user)):
    from app.modules.ai.compliance import check_compliance
    return success(check_compliance(body.category, body.data))
