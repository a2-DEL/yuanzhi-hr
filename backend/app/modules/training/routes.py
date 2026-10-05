"""培训与开发模块路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.training.models import TrainingCourse, TrainingPlan, TrainingRecord, TalentPipeline

router = APIRouter(prefix="/api/training", tags=["培训与开发"])


# ===== 课程库 =====
@router.get("/courses", summary="课程列表")
def course_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(TrainingCourse).filter(TrainingCourse.status == 1).all()
    return success([{
        "id": c.id, "title": c.title, "category": c.category,
        "lecturer": c.lecturer, "hours": float(c.hours) if c.hours else 1,
        "max_students": c.max_students, "description": c.description,
    } for c in items])


class CourseIn(BaseModel):
    title: str
    category: str = "岗位技能"
    description: str = None
    lecturer: str = None
    hours: float = 1
    max_students: int = 30


@router.post("/courses", summary="新增课程")
def add_course(body: CourseIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(TrainingCourse(**body.model_dump()))
    db.commit()
    return success(msg="课程已创建")


# ===== 培训计划/开班 =====
@router.get("/plans", summary="培训计划列表")
def plan_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(TrainingPlan).order_by(TrainingPlan.id.desc()).all()
    return success([{
        "id": p.id, "course_title": p.course_title,
        "start_date": p.start_date.isoformat() if p.start_date else None,
        "end_date": p.end_date.isoformat() if p.end_date else None,
        "location": p.location, "student_count": p.student_count,
        "status": p.status,
    } for p in items])


class PlanIn(BaseModel):
    course_id: int
    course_title: str
    start_date: date = None
    end_date: date = None
    location: str = None


@router.post("/plans", summary="创建培训计划")
def add_plan(body: PlanIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(TrainingPlan(**body.model_dump()))
    db.commit()
    return success(msg="培训计划已创建")


# ===== 学员记录 =====
@router.get("/records", summary="培训记录")
def record_list(plan_id: int = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(TrainingRecord)
    if plan_id:
        q = q.filter(TrainingRecord.plan_id == plan_id)
    items = q.all()
    return success([{
        "id": r.id, "employee_name": r.employee_name,
        "score": r.score, "status": r.status,
    } for r in items])


class RecordIn(BaseModel):
    plan_id: int
    employee_id: int
    employee_name: str


@router.post("/records", summary="报名学员")
def add_record(body: RecordIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(TrainingRecord(**body.model_dump()))
    plan = db.query(TrainingPlan).get(body.plan_id)
    if plan:
        plan.student_count = (plan.student_count or 0) + 1
    db.commit()
    return success(msg="学员已报名")


# ===== 人才梯队 =====
@router.get("/pipeline", summary="人才梯队")
def pipeline_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    items = db.query(TalentPipeline).all()
    return success([{
        "id": t.id, "employee_name": t.employee_name,
        "dept_name": t.dept_name, "target_position": t.target_position,
        "level": t.level, "readiness": t.readiness, "note": t.note,
    } for t in items])


class PipelineIn(BaseModel):
    employee_id: int = None
    employee_name: str
    dept_name: str = None
    target_position: str = None
    level: str = "储备"
    readiness: int = 50
    note: str = None


@router.post("/pipeline", summary="加入人才梯队")
def add_pipeline(body: PipelineIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    db.add(TalentPipeline(**body.model_dump()))
    db.commit()
    return success(msg="已加入人才梯队")
