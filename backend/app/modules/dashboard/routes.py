"""数据可视化大屏聚合接口"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success
from app.core.deps import get_current_user
from app.modules.employee.models import Employee
from app.modules.organization.models import Department
from app.modules.attendance.models import AttendanceRecord, LeaveRequest
from app.modules.salary.models import SalaryRecord
from app.modules.recruitment.models import Resume, RecruitmentDemand
from app.modules.training.models import TrainingPlan, TrainingRecord
from app.modules.performance.models import PerformanceScore
from app.modules.employee_relation.models import Offboarding, LaborContract

router = APIRouter(prefix="/api/dashboard", tags=["数据大屏"])


@router.get("/executive", summary="老板经营大屏核心指标")
def executive_dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    # 员工总数
    total_emp = db.query(Employee).filter(Employee.status == "active").count()

    # 部门数
    dept_count = db.query(Department).filter(Department.status == 1).count()

    # 本月入职/离职
    from datetime import date
    today = date.today()
    month_start = today.replace(day=1)

    # 招聘漏斗
    resume_total = db.query(Resume).count()
    resume_hired = db.query(Resume).filter(Resume.status == "hired").count()
    resume_inverview = db.query(Resume).filter(Resume.status == "interview").count()

    # 考勤异常
    absent = db.query(AttendanceRecord).filter(AttendanceRecord.status == "absent").count()
    leave_pending = db.query(LeaveRequest).filter(LeaveRequest.status == "pending").count()

    # 薪资总成本（最近月）
    latest = db.query(SalaryRecord).order_by(SalaryRecord.salary_month.desc()).first()
    if latest:
        latest_month = latest.salary_month
        records = db.query(SalaryRecord).filter(SalaryRecord.salary_month == latest_month).all()
        total_cost = sum(float(r.gross_salary or 0) for r in records)
    else:
        total_cost = 0

    # 绩效分布
    perf_items = db.query(PerformanceScore).filter(PerformanceScore.final_score.isnot(None)).all()
    perf_dist = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
    for p in perf_items:
        if p.grade in perf_dist:
            perf_dist[p.grade] += 1

    # 培训完成数
    training_done = db.query(TrainingRecord).filter(TrainingRecord.status == "completed").count()

    # 合同到期提醒
    expiring_contracts = db.query(LaborContract).filter(
        LaborContract.end_date.isnot(None)
    ).all()
    expiring_soon = sum(1 for c in expiring_contracts if c.end_date and 0 <= (c.end_date - today).days <= 90)

    # 离职率
    offboard_total = db.query(Offboarding).count()

    # 学历分布
    edu_dist = {}
    active_emps = db.query(Employee).filter(Employee.status == "active").all()
    for e in active_emps:
        edu = e.education or "未知"
        edu_dist[edu] = edu_dist.get(edu, 0) + 1

    # 部门人数分布
    dept_dist = []
    depts = db.query(Department).filter(Department.status == 1).all()
    for d in depts:
        cnt = db.query(Employee).filter(
            Employee.dept_id == d.id, Employee.status == "active"
        ).count()
        dept_dist.append({"name": d.dept_name, "value": cnt, "dept_id": d.id})

    return success({
        "headcount": {
            "total": total_emp,
            "dept_count": dept_count,
            "hired_this_month": resume_hired,
            "offboard_total": offboard_total,
        },
        "recruitment": {
            "resume_total": resume_total,
            "in_interview": resume_inverview,
            "hired": resume_hired,
        },
        "attendance": {
            "absent": absent,
            "leave_pending": leave_pending,
        },
        "cost": {
            "monthly_total": round(total_cost, 2),
            "per_capita": round(total_cost / total_emp, 2) if total_emp else 0,
        },
        "performance": perf_dist,
        "training": {"completed": training_done},
        "compliance": {"expiring_contracts": expiring_soon},
        "edu_distribution": edu_dist,
        "dept_distribution": dept_dist,
    })
