"""员工自助门户路由"""
from fastapi import APIRouter, Depends
from datetime import date, timedelta
from app.core.response import success
from app.core.deps import get_current_user
from app.core.database import SessionLocal
from app.modules.system.models import User
from app.modules.employee.models import Employee
from app.modules.attendance.models import AttendanceRecord, LeaveRequest
from app.modules.salary.models import SalaryRecord
from app.modules.performance.models import PerformanceScore

router = APIRouter(prefix="/api/self", tags=["员工自助"])


def _get_my_emp(db, user):
    """获取当前登录用户对应的员工档案，demo模式下返回第一个员工"""
    emp = db.query(Employee).filter(Employee.user_id == user.id).first()
    if not emp:
        emp = db.query(Employee).first()
    return emp


@router.get("/profile", summary="我的档案")
def my_profile(user: User = Depends(get_current_user)):
    db = SessionLocal()
    emp = _get_my_emp(db, user)
    dept_name = ""
    if emp and emp.dept_id:
        from app.modules.organization.models import Department
        dept = db.query(Department).filter(Department.id == emp.dept_id).first()
        dept_name = dept.dept_name if dept else ""
    db.close()
    if not emp:
        return success({})
    return success({
        "name": emp.name,
        "emp_no": emp.emp_no,
        "dept": dept_name,
        "position": emp.position,
        "entry_date": str(emp.entry_date),
        "phone": emp.phone,
        "email": emp.email or "",
    })


@router.get("/attendance", summary="我的考勤（最近30天）")
def my_attendance(user: User = Depends(get_current_user)):
    db = SessionLocal()
    emp = _get_my_emp(db, user)
    if not emp:
        db.close()
        return success({"records": [], "stats": {}})
    records = db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == emp.id
    ).order_by(AttendanceRecord.attendance_date.desc()).limit(30).all()
    db.close()
    return success({
        "records": [{"date": str(r.attendance_date), "check_in": str(r.clock_in) if r.clock_in else "", "check_out": str(r.clock_out) if r.clock_out else "", "status": r.status} for r in records],
        "stats": {
            "total": len(records),
            "normal": len([r for r in records if r.status == "normal"]),
            "late": len([r for r in records if r.status == "late"]),
        }
    })


@router.get("/leaves", summary="我的请假记录")
def my_leaves(user: User = Depends(get_current_user)):
    db = SessionLocal()
    emp = _get_my_emp(db, user)
    if not emp:
        db.close()
        return success([])
    leaves = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == emp.id
    ).order_by(LeaveRequest.create_time.desc()).all()
    db.close()
    return success([{
        "id": l.id, "type": l.leave_type, "days": l.days,
        "reason": l.reason, "status": l.status,
        "start_date": str(l.start_date), "end_date": str(l.end_date),
    } for l in leaves])


@router.post("/leave", summary="提交请假申请")
def apply_leave(data: dict, user: User = Depends(get_current_user)):
    db = SessionLocal()
    emp = _get_my_emp(db, user)
    if not emp:
        db.close()
        return success({}, message="请先完善员工档案")
    from datetime import datetime
    leave = LeaveRequest(
        employee_id=emp.id,
        leave_type=data.get("type", "事假"),
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d").date(),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d").date(),
        days=data.get("days", 1),
        reason=data.get("reason", ""),
        status="pending",
    )
    db.add(leave)
    db.commit()
    db.close()
    return success({}, message="请假申请已提交")


@router.get("/salary", summary="我的工资条（最近6个月）")
def my_salary(user: User = Depends(get_current_user)):
    db = SessionLocal()
    emp = _get_my_emp(db, user)
    if not emp:
        db.close()
        return success([])
    records = db.query(SalaryRecord).filter(
        SalaryRecord.employee_id == emp.id
    ).order_by(SalaryRecord.salary_month.desc()).limit(6).all()
    db.close()
    return success([{
        "period": r.salary_month,
        "base": float(r.base_salary),
        "bonus": float(r.performance_salary) + float(r.allowance),
        "deduction": float(r.deduct),
        "social": float(r.social_insurance),
        "housing": float(r.housing_fund),
        "tax": float(r.tax),
        "net": float(r.net_salary),
    } for r in records])


@router.get("/performance", summary="我的绩效")
def my_performance(user: User = Depends(get_current_user)):
    db = SessionLocal()
    emp = _get_my_emp(db, user)
    if not emp:
        db.close()
        return success([])
    scores = db.query(PerformanceScore).filter(
        PerformanceScore.employee_id == emp.id
    ).order_by(PerformanceScore.create_time.desc()).all()
    db.close()
    return success([{
        "period": s.period, "level": s.level,
        "score": s.score, "comment": s.comment or "",
    } for s in scores])


@router.get("/dashboard", summary="员工自助首页统计")
def my_dashboard(user: User = Depends(get_current_user)):
    db = SessionLocal()
    emp = _get_my_emp(db, user)
    if not emp:
        db.close()
        return success({})
    pending_leaves = db.query(LeaveRequest).filter(
        LeaveRequest.employee_id == emp.id, LeaveRequest.status == "pending"
    ).count()
    db.close()
    return success({
        "pending_leaves": pending_leaves,
        "year_leave_balance": 5,  # 示例：年假余额
        "sick_leave_balance": 3,
    })
