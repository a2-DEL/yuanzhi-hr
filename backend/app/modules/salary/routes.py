"""薪酬模块路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.salary.models import SalaryRecord, SalaryStructure
from app.modules.employee.models import Employee

router = APIRouter(prefix="/api/salary", tags=["薪酬管理"])


@router.get("/records", summary="工资表列表")
def record_list(month: str = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(SalaryRecord)
    if month:
        q = q.filter(SalaryRecord.salary_month == month)
    records = q.order_by(SalaryRecord.id.desc()).all()
    # 非管理员隐藏他人薪资明细（字段级脱敏）
    result = []
    for r in records:
        item = {
            "id": r.id, "employee_id": r.employee_id,
            "month": r.salary_month, "status": r.status,
            "gross": float(r.gross_salary or 0),
        }
        if user.is_superuser:
            item.update({
                "base": float(r.base_salary or 0),
                "performance": float(r.performance_salary or 0),
                "allowance": float(r.allowance or 0),
                "social": float(r.social_insurance or 0),
                "fund": float(r.housing_fund or 0),
                "tax": float(r.tax or 0),
                "net": float(r.net_salary or 0),
            })
        result.append(item)
    return success(result)


@router.post("/calculate", summary="一键核算月度工资")
def calculate(month: str, db: Session = Depends(get_db), _=Depends(get_current_user)):
    """简易核算：基于员工基本工资计算"""
    employees = db.query(Employee).filter(Employee.status == "active").all()
    count = 0
    for emp in employees:
        # 检查是否已存在
        existing = db.query(SalaryRecord).filter(
            SalaryRecord.employee_id == emp.id,
            SalaryRecord.salary_month == month
        ).first()
        if existing:
            continue
        base = float(emp.base_salary or 0)
        social = round(base * 0.105, 2)   # 养老8%+医疗2%+失业0.5%
        fund = round(base * 0.07, 2)
        gross = base
        tax = 0  # 简化：低于起征点不计税
        net = gross - social - fund - tax
        db.add(SalaryRecord(
            employee_id=emp.id, salary_month=month,
            base_salary=base, performance_salary=0, allowance=0,
            social_insurance=social, housing_fund=fund, tax=tax, deduct=0,
            gross_salary=gross, net_salary=net,
        ))
        count += 1
    db.commit()
    return success({"created": count, "month": month}, f"已核算 {count} 名员工 {month} 工资")


@router.get("/structures", summary="薪资结构列表")
def structure_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(SalaryStructure).all()
    return success([{
        "id": i.id, "employee_id": i.employee_id,
        "base": float(i.base_salary or 0),
        "position": float(i.position_salary or 0),
        "performance": float(i.performance_salary or 0),
    } for i in items])


class StructureIn(BaseModel):
    employee_id: int
    base_salary: float = 0
    position_salary: float = 0
    performance_salary: float = 0


@router.post("/structures", summary="设置薪资结构")
def set_structure(body: StructureIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    existing = db.query(SalaryStructure).filter(SalaryStructure.employee_id == body.employee_id).first()
    if existing:
        for k, v in body.model_dump().items():
            setattr(existing, k, v)
    else:
        db.add(SalaryStructure(**body.model_dump()))
    db.commit()
    return success(msg="薪资结构已保存")
