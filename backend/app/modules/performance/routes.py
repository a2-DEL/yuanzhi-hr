"""绩效管理模块路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.performance.models import KpiIndicator, PerformanceCycle, PerformanceScore

router = APIRouter(prefix="/api/performance", tags=["绩效管理"])


# ===== KPI指标库 =====
@router.get("/indicators", summary="KPI指标列表")
def indicator_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(KpiIndicator).filter(KpiIndicator.status == 1).all()
    return success([{
        "id": i.id, "name": i.name, "department": i.department,
        "weight": float(i.weight) if i.weight else 0,
        "target": i.target, "calculation": i.calculation,
    } for i in items])


class IndicatorIn(BaseModel):
    name: str
    department: str = None
    weight: float = 0
    target: str = None
    calculation: str = None


@router.post("/indicators", summary="新增KPI指标")
def add_indicator(body: IndicatorIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(KpiIndicator(**body.model_dump()))
    db.commit()
    return success(msg="指标已创建")


# ===== 考核周期 =====
@router.get("/cycles", summary="考核周期列表")
def cycle_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(PerformanceCycle).order_by(PerformanceCycle.id.desc()).all()
    return success([{
        "id": c.id, "name": c.name, "type": c.type,
        "start_date": c.start_date, "end_date": c.end_date,
        "status": c.status,
    } for c in items])


class CycleIn(BaseModel):
    name: str
    type: str = "quarterly"
    start_date: str = None
    end_date: str = None


@router.post("/cycles", summary="创建考核周期")
def add_cycle(body: CycleIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(PerformanceCycle(**body.model_dump()))
    db.commit()
    return success(msg="考核周期已创建")


# ===== 绩效评分 =====
@router.get("/scores", summary="绩效评分列表")
def score_list(cycle_id: int = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(PerformanceScore)
    if cycle_id:
        q = q.filter(PerformanceScore.cycle_id == cycle_id)
    items = q.all()
    return success([{
        "id": s.id, "employee_name": s.employee_name,
        "dept_name": s.dept_name,
        "self_score": float(s.self_score) if s.self_score else None,
        "manager_score": float(s.manager_score) if s.manager_score else None,
        "final_score": float(s.final_score) if s.final_score else None,
        "grade": s.grade, "status": s.status, "comment": s.comment,
    } for s in items])


class ScoreIn(BaseModel):
    cycle_id: int
    employee_name: str
    dept_name: str = None
    self_score: float = None
    manager_score: float = None
    comment: str = None


@router.post("/scores", summary="录入/提交绩效评分")
def add_score(body: ScoreIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    data = body.model_dump()
    # 自动计算最终得分与等级
    final = None
    grade = None
    if data.get("manager_score") is not None:
        final = data["manager_score"]
    elif data.get("self_score") is not None:
        final = data["self_score"]
    if final is not None:
        if final >= 90: grade = "S"
        elif final >= 80: grade = "A"
        elif final >= 70: grade = "B"
        elif final >= 60: grade = "C"
        else: grade = "D"
    data["final_score"] = final
    data["grade"] = grade
    db.add(PerformanceScore(**data))
    db.commit()
    return success(msg="绩效评分已提交", data={"grade": grade, "final_score": final})


# ===== 绩效分布统计 =====
@router.get("/distribution", summary="绩效等级分布")
def distribution(cycle_id: int = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(PerformanceScore).filter(PerformanceScore.final_score.isnot(None))
    if cycle_id:
        q = q.filter(PerformanceScore.cycle_id == cycle_id)
    items = q.all()
    dist = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
    for s in items:
        if s.grade in dist:
            dist[s.grade] += 1
    return success({"distribution": dist, "total": len(items)})
