"""考勤模块路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, datetime
from pydantic import BaseModel
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.attendance.models import LeaveRequest, AttendanceRecord, LeaveBalance

router = APIRouter(prefix="/api/attendance", tags=["考勤管理"])


@router.get("/leave/list", summary="请假列表")
def leave_list(db: Session = Depends(get_db), _=Depends(get_current_user)):
    records = db.query(LeaveRequest).order_by(LeaveRequest.id.desc()).all()
    return success([{
        "id": r.id, "employee_id": r.employee_id,
        "leave_type": r.leave_type,
        "start_date": r.start_date.isoformat(),
        "end_date": r.end_date.isoformat(),
        "days": float(r.days), "reason": r.reason,
        "status": r.status,
        "create_time": r.create_time.strftime("%Y-%m-%d %H:%M") if r.create_time else None,
    } for r in records])


class LeaveIn(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    days: float = 1
    reason: str = None


@router.post("/leave", summary="提交请假申请")
def add_leave(body: LeaveIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    r = LeaveRequest(**body.model_dump())
    db.add(r); db.commit()
    return success(msg="请假申请已提交")


@router.put("/leave/{leave_id}/approve", summary="审批请假")
def approve_leave(leave_id: int, action: str = "approve", db: Session = Depends(get_db), _=Depends(get_current_user)):
    r = db.query(LeaveRequest).get(leave_id)
    if not r: raise AppException(message="记录不存在")
    r.status = "approved" if action == "approve" else "rejected"
    r.approve_time = datetime.now()
    db.commit()
    return success(msg="审批完成")


@router.get("/records", summary="打卡记录")
def records(db: Session = Depends(get_db), _=Depends(get_current_user)):
    records = db.query(AttendanceRecord).order_by(AttendanceRecord.id.desc()).limit(50).all()
    return success([{
        "id": r.id, "employee_id": r.employee_id,
        "date": r.attendance_date.isoformat(),
        "clock_in": r.clock_in.strftime("%H:%M") if r.clock_in else None,
        "clock_out": r.clock_out.strftime("%H:%M") if r.clock_out else None,
        "status": r.status,
    } for r in records])


class ClockIn(BaseModel):
    employee_id: int


@router.post("/clock-in", summary="上班打卡")
def clock_in(body: ClockIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    today = date.today()
    existing = db.query(AttendanceRecord).filter(
        AttendanceRecord.employee_id == body.employee_id,
        AttendanceRecord.attendance_date == today
    ).first()
    if existing and existing.clock_in:
        raise AppException(message="今日已打卡")
    if existing:
        existing.clock_in = datetime.now()
    else:
        db.add(AttendanceRecord(
            employee_id=body.employee_id, attendance_date=today,
            clock_in=datetime.now()
        ))
    db.commit()
    return success(msg="打卡成功")
