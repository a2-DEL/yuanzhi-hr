"""培训与开发模块数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, Date, Numeric
from datetime import datetime
from app.core.database import Base


class TrainingCourse(Base):
    """培训课程库"""
    __tablename__ = "training_course"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False, comment="课程名称")
    category = Column(String(64), comment="类别：新员工/岗位技能/管理/安全")
    description = Column(Text, comment="课程描述")
    lecturer = Column(String(64), comment="讲师")
    hours = Column(Numeric(5, 1), default=1, comment="课时")
    max_students = Column(Integer, default=30, comment="上限人数")
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, default=datetime.now)


class TrainingPlan(Base):
    """培训计划/开班记录"""
    __tablename__ = "training_plan"
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, comment="关联课程")
    course_title = Column(String(128), comment="课程名称（冗余）")
    start_date = Column(Date, comment="开始日期")
    end_date = Column(Date, comment="结束日期")
    location = Column(String(128), comment="地点/线上链接")
    student_count = Column(Integer, default=0, comment="已报名人数")
    status = Column(String(20), default="planned", comment="planned/ongoing/completed")
    create_time = Column(DateTime, default=datetime.now)


class TrainingRecord(Base):
    """学员培训记录"""
    __tablename__ = "training_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, comment="关联培训计划")
    employee_id = Column(Integer, comment="学员")
    employee_name = Column(String(64))
    score = Column(Integer, comment="考核成绩")
    status = Column(String(20), default="enrolled", comment="enrolled/completed/failed")
    create_time = Column(DateTime, default=datetime.now)


class TalentPipeline(Base):
    """人才梯队/储备干部"""
    __tablename__ = "training_talent_pipeline"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    employee_name = Column(String(64))
    dept_name = Column(String(128))
    target_position = Column(String(128), comment="目标岗位")
    level = Column(String(20), comment="梯队层级：储备/后备/继任")
    readiness = Column(Integer, default=0, comment="就绪度0-100")
    note = Column(String(255))
    create_time = Column(DateTime, default=datetime.now)
