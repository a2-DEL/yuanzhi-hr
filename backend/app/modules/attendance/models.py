"""考勤模块数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, SmallInteger, Text, ForeignKey
from datetime import datetime
from app.core.database import Base


class LeaveBalance(Base):
    """员工假期额度"""
    __tablename__ = "attendance_leave_balance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("hr_employee.id"), nullable=False)
    year = Column(Integer, nullable=False)
    annual_leave_total = Column(Numeric(5, 1), default=0, comment="年假总额")
    annual_leave_used = Column(Numeric(5, 1), default=0, comment="已休年假")
    personal_leave_used = Column(Numeric(5, 1), default=0, comment="事假已用")
    sick_leave_used = Column(Numeric(5, 1), default=0, comment="病假已用")
    create_time = Column(DateTime, default=datetime.now)


class LeaveRequest(Base):
    """请假申请"""
    __tablename__ = "attendance_leave_request"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("hr_employee.id"), nullable=False)
    leave_type = Column(String(32), comment="annual/personal/sick/marriage/bereavement")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    days = Column(Numeric(4, 1), default=1)
    reason = Column(Text)
    status = Column(String(20), default="pending", comment="pending/approved/rejected")
    approver_id = Column(Integer)
    approve_time = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)


class AttendanceRecord(Base):
    """打卡记录"""
    __tablename__ = "attendance_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("hr_employee.id"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    clock_in = Column(DateTime, comment="上班打卡")
    clock_out = Column(DateTime, comment="下班打卡")
    status = Column(String(20), default="normal", comment="normal/late/early/absent")
    remark = Column(String(255))
    create_time = Column(DateTime, default=datetime.now)
