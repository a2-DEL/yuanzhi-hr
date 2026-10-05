"""AI自动报表：自然语言提问→自动生成图表数据"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.response import success
from app.core.deps import get_current_user
from app.core.database import SessionLocal
from app.modules.employee.models import Employee
from app.modules.performance.models import PerformanceScore
from app.modules.recruitment.models import Resume

router = APIRouter(prefix="/api/report", tags=["AI自动报表"])


class ReportQueryIn(BaseModel):
    question: str


@router.post("/generate", summary="自然语言生成报表")
def generate_report(body: ReportQueryIn, _=Depends(get_current_user)):
    q = body.question.lower()
    db = SessionLocal()

    chart_type = "bar"
    title = ""
    labels = []
    values = []

    if "部门" in q and "人数" in q:
        title = "各部门人数分布"
        from app.modules.organization.models import Department
        depts = db.query(Department).filter(Department.status == 1).all()
        for d in depts:
            labels.append(d.dept_name)
            values.append(db.query(Employee).filter(
                Employee.dept_id == d.id, Employee.status == "active"
            ).count())

    elif "绩效" in q:
        title = "绩效等级分布"
        scores = db.query(PerformanceScore).all()
        dist = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
        for s in scores:
            if s.level in dist:
                dist[s.level] += 1
        labels = list(dist.keys())
        values = list(dist.values())
        chart_type = "pie"

    elif "招聘" in q or "简历" in q:
        title = "招聘漏斗"
        labels = ["简历总数", "面试中", "已入职"]
        values = [
            db.query(Resume).count(),
            db.query(Resume).filter(Resume.status == "interview").count(),
            db.query(Resume).filter(Resume.status == "hired").count(),
        ]
        chart_type = "funnel"

    else:
        title = "员工总数概览"
        labels = ["在职员工"]
        values = [db.query(Employee).filter(Employee.status == "active").count()]

    db.close()
    return success({
        "title": title,
        "chart_type": chart_type,
        "data": {"labels": labels, "values": values},
        "question": body.question,
    })
