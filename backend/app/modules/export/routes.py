"""数据导入导出路由"""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
import csv
import io
from app.core.response import success
from app.core.deps import get_current_user
from app.core.database import SessionLocal
from app.modules.employee.models import Employee

router = APIRouter(prefix="/api/export", tags=["数据导出"])


@router.get("/employees", summary="导出员工CSV")
def export_employees(_=Depends(get_current_user)):
    db = SessionLocal()
    emps = db.query(Employee).all()
    db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["工号", "姓名", "性别", "手机号", "部门", "职位", "员工类型", "入职日期", "状态"])
    for e in emps:
        writer.writerow([
            e.emp_no, e.name, e.gender, e.phone,
            e.dept.dept_name if e.dept else "", e.position,
            e.employee_type, str(e.entry_date) if e.entry_date else "",
            e.status,
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=employees.csv"}
    )


@router.get("/salary", summary="导出工资表CSV")
def export_salary(period: str = None, _=Depends(get_current_user)):
    from app.modules.salary.models import SalaryRecord
    db = SessionLocal()
    q = db.query(SalaryRecord)
    if period:
        q = q.filter(SalaryRecord.period == period)
    records = q.all()
    db.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["周期", "工号", "姓名", "基本工资", "奖金", "社保", "公积金", "个税", "实发"])
    for r in records:
        writer.writerow([
            r.period, r.employee.emp_no, r.employee.name,
            r.base_salary, r.bonus, r.social_insurance,
            r.housing_fund, r.tax, r.net_salary,
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=salary.csv"}
    )
