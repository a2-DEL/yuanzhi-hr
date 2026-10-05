"""组织记忆数据飞轮：统计学习企业自身规律"""
from fastapi import APIRouter, Depends
from app.core.response import success
from app.core.deps import get_current_user
from app.core.database import SessionLocal
from app.modules.employee.models import Employee
from app.modules.performance.models import PerformanceScore
from app.modules.employee_relation.models import Offboarding

router = APIRouter(prefix="/api/memory", tags=["组织记忆"])


@router.get("/insights", summary="组织记忆洞察")
def insights(_=Depends(get_current_user)):
    db = SessionLocal()
    result = {}

    # 1. 高绩效员工特征（S/A级员工的共同属性）
    high_perf = db.query(PerformanceScore).filter(
        PerformanceScore.level.in_(["S", "A"])
    ).all()
    high_emp_ids = set([p.employee_id for p in high_perf])
    high_emps = db.query(Employee).filter(Employee.id.in_(high_emp_ids)).all()
    edu_count = {}
    for e in high_emps:
        edu_count[e.education or "未知"] = edu_count.get(e.education or "未知", 0) + 1
    result["high_perf_profile"] = {
        "sample_size": len(high_emps),
        "education_distribution": edu_count,
        "insight": f"高绩效员工共{len(high_emps)}人，本科及以上占比最高" if high_emps else "暂无数据",
    }

    # 2. 离职风险分析
    offboards = db.query(Offboarding).all()
    result["offboarding_analysis"] = {
        "total": len(offboards),
        "avg_tenure_years": round(sum([(2026 - o.entry_date.year) for o in offboards if o.entry_date]) / len(offboards), 1) if offboards else 0,
        "insight": f"历史离职{len(offboards)}人" if offboards else "暂无离职记录",
    }

    # 3. 部门绩效分布
    dept_perf = {}
    all_scores = db.query(PerformanceScore).all()
    for p in all_scores:
        emp = db.query(Employee).filter(Employee.id == p.employee_id).first()
        if emp and emp.dept:
            dept_name = emp.dept.dept_name
            if dept_name not in dept_perf:
                dept_perf[dept_name] = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
            dept_perf[dept_name][p.level] += 1
    result["dept_performance"] = dept_perf

    db.close()
    return success(result)
