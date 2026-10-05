"""员工档案路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.employee.models import Employee
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/api/employee", tags=["员工档案"])


@router.get("/list", summary="员工列表")
def emp_list(dept_id: int = None, status: str = None, keyword: str = None,
             db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(Employee)

    # 行级权限：部门经理只看本部门员工
    user_roles = [r.role_code for r in user.roles]
    if "DEPT_MANAGER" in user_roles and not user.is_superuser:
        # 部门经理：只看自己所在部门的员工
        if user.dept_id:
            q = q.filter(Employee.dept_id == user.dept_id)
    elif "EMPLOYEE" in user_roles and not user.is_superuser:
        # 普通员工：只看自己
        q = q.filter(Employee.user_id == user.id)

    if dept_id: q = q.filter(Employee.dept_id == dept_id)
    if status: q = q.filter(Employee.status == status)
    if keyword: q = q.filter(Employee.name.like(f"%{keyword}%"))
    emps = q.order_by(Employee.id.desc()).all()

    # 字段级脱敏：非管理员隐藏薪资
    hide_salary = not user.is_superuser
    result = []
    for e in emps:
        item = {
            "id": e.id, "emp_no": e.emp_no, "name": e.name,
            "gender": e.gender, "phone": e.phone, "email": e.email,
            "dept_id": e.dept_id, "position": e.position,
            "employee_type": e.employee_type, "status": e.status,
            "entry_date": e.entry_date.isoformat() if e.entry_date else None,
            "education": e.education, "emergency_contact": e.emergency_contact,
        }
        if not hide_salary:
            item["base_salary"] = float(e.base_salary) if e.base_salary else None
        result.append(item)
    return result and success(result) or success([])


class EmployeeIn(BaseModel):
    emp_no: str
    name: str
    gender: int = 1
    phone: str = None
    email: str = None
    dept_id: int = None
    position: str = None
    employee_type: str = "正式"
    entry_date: date = None
    contract_start: date = None
    contract_end: date = None
    education: str = None
    graduation_school: str = None
    major: str = None
    emergency_contact: str = None
    emergency_phone: str = None
    base_salary: float = None


@router.post("", summary="新增员工")
def add_emp(body: EmployeeIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    e = Employee(**body.model_dump())
    db.add(e); db.commit()
    return success(msg="员工创建成功")


@router.get("/{emp_id}", summary="员工详情")
def emp_detail(emp_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    e = db.query(Employee).get(emp_id)
    if not e: raise AppException(message="员工不存在")
    data = {
        "id": e.id, "emp_no": e.emp_no, "name": e.name,
        "gender": e.gender, "birthday": e.birthday.isoformat() if e.birthday else None,
        "id_card": e.id_card, "phone": e.phone, "email": e.email,
        "dept_id": e.dept_id, "position": e.position,
        "employee_type": e.employee_type, "status": e.status,
        "entry_date": e.entry_date.isoformat() if e.entry_date else None,
    }
    if user.is_superuser:
        data["base_salary"] = float(e.base_salary) if e.base_salary else None
    return success(data)
