"""人力资源规划模块路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.planning.models import HeadcountBudget, JobDescription, PolicyDoc
from app.modules.organization.models import Department
from app.modules.employee.models import Employee

router = APIRouter(prefix="/api/planning", tags=["人力资源规划"])


# ===== 编制管理 =====
@router.get("/headcount", summary="编制与实际人数对比")
def headcount(db: Session = Depends(get_db), _=Depends(get_current_user)):
    depts = db.query(Department).filter(Department.status == 1).all()
    result = []
    for d in depts:
        budget = db.query(HeadcountBudget).filter(
            HeadcountBudget.dept_id == d.id,
            HeadcountBudget.year == 2026
        ).first()
        actual = db.query(Employee).filter(
            Employee.dept_id == d.id,
            Employee.status == "active"
        ).count()
        result.append({
            "dept_id": d.id, "dept_name": d.dept_name,
            "budget": budget.budget_count if budget else 0,
            "actual": actual,
            "difference": (budget.budget_count if budget else 0) - actual,
            "over_budget": actual > (budget.budget_count if budget else 0),
        })
    return success(result)


class BudgetIn(BaseModel):
    dept_id: int
    year: int = 2026
    budget_count: int = 0
    budget_cost: int = 0
    note: str = None


@router.post("/headcount", summary="设置部门编制")
def set_budget(body: BudgetIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    existing = db.query(HeadcountBudget).filter(
        HeadcountBudget.dept_id == body.dept_id,
        HeadcountBudget.year == body.year
    ).first()
    if existing:
        existing.budget_count = body.budget_count
        existing.budget_cost = body.budget_cost
        existing.note = body.note
    else:
        db.add(HeadcountBudget(**body.model_dump()))
    db.commit()
    return success(msg="编制已保存")


# ===== 岗位说明书 =====
@router.get("/jobs", summary="岗位说明书列表")
def job_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    jobs = db.query(JobDescription).filter(JobDescription.status == 1).all()
    return success([{
        "id": j.id, "title": j.title, "dept_id": j.dept_id,
        "responsibilities": j.responsibilities,
        "requirements": j.requirements, "salary_range": j.salary_range,
    } for j in jobs])


class JobIn(BaseModel):
    title: str
    dept_id: int = None
    responsibilities: str = None
    requirements: str = None
    salary_range: str = None


@router.post("/jobs", summary="新增岗位说明书")
def add_job(body: JobIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(JobDescription(**body.model_dump()))
    db.commit()
    return success(msg="岗位说明书已创建")


# ===== 制度文档库 =====
@router.get("/policies", summary="制度文档列表")
def policy_list(category: str = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(PolicyDoc).filter(PolicyDoc.status == 1)
    if category:
        q = q.filter(PolicyDoc.category == category)
    docs = q.all()
    return success([{
        "id": d.id, "title": d.title, "category": d.category,
        "version": d.version, "content": d.content,
        "create_time": d.create_time.strftime("%Y-%m-%d") if d.create_time else None,
    } for d in docs])


class PolicyIn(BaseModel):
    title: str
    category: str
    content: str = None


@router.post("/policies", summary="新增制度文档")
def add_policy(body: PolicyIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(PolicyDoc(**body.model_dump()))
    db.commit()
    return success(msg="制度已保存")
