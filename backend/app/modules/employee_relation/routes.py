"""员工关系管理模块路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date, timedelta
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.employee_relation.models import LaborContract, EmployeeTransfer, Discipline, Offboarding

router = APIRouter(prefix="/api/employee-relation", tags=["员工关系"])


# ===== 劳动合同 =====
@router.get("/contracts", summary="合同列表（含到期提醒）")
def contract_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(LaborContract).order_by(LaborContract.end_date.asc()).all()
    today = date.today()
    result = []
    for c in items:
        days_left = None
        if c.end_date:
            days_left = (c.end_date - today).days
        result.append({
            "id": c.id, "employee_name": c.employee_name,
            "contract_type": c.contract_type,
            "start_date": c.start_date.isoformat() if c.start_date else None,
            "end_date": c.end_date.isoformat() if c.end_date else "无固定期限",
            "status": c.status, "days_left": days_left,
            "expiring_soon": days_left is not None and 0 <= days_left <= 90,
        })
    return success(result)


class ContractIn(BaseModel):
    employee_id: int = None
    employee_name: str
    contract_type: str = "固定期限"
    start_date: date = None
    end_date: date = None
    sign_date: date = None


@router.post("/contracts", summary="登记劳动合同")
def add_contract(body: ContractIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(LaborContract(**body.model_dump()))
    db.commit()
    return success(msg="合同已登记")


# ===== 入转调离 =====
@router.get("/transfers", summary="异动记录")
def transfer_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(EmployeeTransfer).order_by(EmployeeTransfer.id.desc()).all()
    return success([{
        "id": t.id, "employee_name": t.employee_name,
        "change_type": t.change_type,
        "from_dept": t.from_dept, "to_dept": t.to_dept,
        "from_position": t.from_position, "to_position": t.to_position,
        "effective_date": t.effective_date.isoformat() if t.effective_date else None,
        "reason": t.reason,
    } for t in items])


class TransferIn(BaseModel):
    employee_name: str
    change_type: str = "入职"
    from_dept: str = None
    to_dept: str = None
    from_position: str = None
    to_position: str = None
    effective_date: date = None
    reason: str = None


@router.post("/transfers", summary="登记异动")
def add_transfer(body: TransferIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(EmployeeTransfer(**body.model_dump()))
    db.commit()
    return success(msg="异动已记录")


# ===== 奖惩记录 =====
@router.get("/disciplines", summary="奖惩记录")
def discipline_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(Discipline).order_by(Discipline.id.desc()).all()
    return success([{
        "id": d.id, "employee_name": d.employee_name,
        "type": d.type, "title": d.title,
        "description": d.description,
        "occur_date": d.occur_date.isoformat() if d.occur_date else None,
    } for d in items])


class DisciplineIn(BaseModel):
    employee_name: str
    type: str = "奖励"
    title: str
    description: str = None
    occur_date: date = None
    approver: str = None


@router.post("/disciplines", summary="登记奖惩")
def add_discipline(body: DisciplineIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(Discipline(**body.model_dump()))
    db.commit()
    return success(msg="奖惩已登记")


# ===== 离职管理 =====
@router.get("/offboardings", summary="离职列表")
def offboarding_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(Offboarding).order_by(Offboarding.id.desc()).all()
    return success([{
        "id": o.id, "employee_name": o.employee_name,
        "dept_name": o.dept_name, "position": o.position,
        "resign_date": o.resign_date.isoformat() if o.resign_date else None,
        "last_day": o.last_day.isoformat() if o.last_day else None,
        "reason_category": o.reason_category,
        "reason_detail": o.reason_detail,
        "status": o.status,
    } for o in items])


class OffboardingIn(BaseModel):
    employee_name: str
    dept_name: str = None
    position: str = None
    resign_date: date = None
    last_day: date = None
    reason_category: str = "其他"
    reason_detail: str = None


@router.post("/offboardings", summary="登记离职")
def add_offboarding(body: OffboardingIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(Offboarding(**body.model_dump()))
    db.commit()
    return success(msg="离职已登记")


# ===== 离职原因统计 =====
@router.get("/attrition-stats", summary="离职原因统计")
def attrition_stats(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(Offboarding).all()
    stats = {}
    for o in items:
        cat = o.reason_category or "未知"
        stats[cat] = stats.get(cat, 0) + 1
    return success({"total": len(items), "by_reason": stats})
