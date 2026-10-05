"""招聘与配置模块路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.recruitment.models import RecruitmentDemand, Resume, Interview, Offer

router = APIRouter(prefix="/api/recruitment", tags=["招聘管理"])


# ===== 招聘需求 =====
@router.get("/demands", summary="招聘需求列表")
def demand_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(RecruitmentDemand).order_by(RecruitmentDemand.id.desc()).all()
    return success([{
        "id": d.id, "title": d.title, "dept_id": d.dept_id,
        "headcount": d.headcount, "salary_range": d.salary_range,
        "channel": d.channel, "status": d.status,
        "expected_date": d.expected_date.isoformat() if d.expected_date else None,
    } for d in items])


class DemandIn(BaseModel):
    title: str
    dept_id: int = None
    headcount: int = 1
    salary_range: str = None
    requirements: str = None
    channel: str = "BOSS直聘"
    expected_date: date = None


@router.post("/demands", summary="新增招聘需求")
def add_demand(body: DemandIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(RecruitmentDemand(**body.model_dump()))
    db.commit()
    return success(msg="招聘需求已发布")


# ===== 简历库 =====
@router.get("/resumes", summary="简历列表")
def resume_list(status: str = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(Resume)
    if status:
        q = q.filter(Resume.status == status)
    items = q.order_by(Resume.id.desc()).all()
    return success([{
        "id": r.id, "candidate_name": r.candidate_name, "phone": r.phone,
        "education": r.education, "school": r.school,
        "current_company": r.current_company, "current_position": r.current_position,
        "status": r.status, "match_score": r.match_score,
        "demand_id": r.demand_id,
    } for r in items])


class ResumeIn(BaseModel):
    demand_id: int = None
    candidate_name: str
    phone: str = None
    email: str = None
    education: str = None
    school: str = None
    major: str = None
    work_years: int = 0
    current_company: str = None
    current_position: str = None
    skills: str = None
    source: str = None


@router.post("/resumes", summary="录入简历")
def add_resume(body: ResumeIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(Resume(**body.model_dump()))
    db.commit()
    return success(msg="简历已录入")


@router.put("/resumes/{resume_id}/status", summary="更新简历状态")
def update_resume_status(resume_id: int, status: str, db: Session = Depends(get_db), _=Depends(get_current_user)):
    r = db.query(Resume).get(resume_id)
    if not r:
        raise AppException(message="简历不存在")
    r.status = status
    db.commit()
    return success(msg="状态已更新")


# ===== 面试安排 =====
@router.get("/interviews", summary="面试列表")
def interview_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(Interview).order_by(Interview.id.desc()).all()
    return success([{
        "id": i.id, "candidate_name": i.candidate_name,
        "interviewer": i.interviewer,
        "interview_time": i.interview_time.isoformat() if i.interview_time else None,
        "location": i.location, "result": i.result,
    } for i in items])


class InterviewIn(BaseModel):
    resume_id: int
    candidate_name: str
    interviewer: str = None
    interview_time: str = None
    location: str = None


@router.post("/interviews", summary="安排面试")
def add_interview(body: InterviewIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    from datetime import datetime
    data = body.model_dump()
    if data.get("interview_time"):
        data["interview_time"] = datetime.fromisoformat(data["interview_time"])
    db.add(Interview(**data))
    db.commit()
    return success(msg="面试已安排")


# ===== 招聘漏斗统计 =====
@router.get("/funnel", summary="招聘漏斗统计")
def funnel(db: Session = Depends(get_db), _=Depends(get_current_user)):
    total = db.query(Resume).count()
    screening = db.query(Resume).filter(Resume.status.in_(["screening", "interview"])).count()
    interview = db.query(Resume).filter(Resume.status == "interview").count()
    offer = db.query(Resume).filter(Resume.status == "offer").count()
    hired = db.query(Resume).filter(Resume.status == "hired").count()
    return success({
        "total": total, "screening": screening,
        "interview": interview, "offer": offer, "hired": hired,
    })
