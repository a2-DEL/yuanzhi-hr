"""招聘与配置模块数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, Date, Numeric
from datetime import datetime
from app.core.database import Base


class RecruitmentDemand(Base):
    """招聘需求"""
    __tablename__ = "recruitment_demand"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False, comment="职位名称")
    dept_id = Column(Integer, comment="需求部门")
    headcount = Column(Integer, default=1, comment="招聘人数")
    salary_range = Column(String(64), comment="薪资范围")
    requirements = Column(Text, comment="任职要求")
    channel = Column(String(64), comment="招聘渠道：BOSS/智联/内推/校招")
    status = Column(String(20), default="open", comment="open/closed/draft")
    creator_id = Column(Integer)
    expected_date = Column(Date, comment="期望到岗日期")
    create_time = Column(DateTime, default=datetime.now)


class Resume(Base):
    """简历库"""
    __tablename__ = "recruitment_resume"
    id = Column(Integer, primary_key=True, autoincrement=True)
    demand_id = Column(Integer, comment="关联招聘需求")
    candidate_name = Column(String(64), nullable=False, comment="候选人姓名")
    phone = Column(String(20))
    email = Column(String(128))
    education = Column(String(32), comment="最高学历")
    school = Column(String(128))
    major = Column(String(64))
    work_years = Column(Integer, default=0, comment="工作年限")
    current_company = Column(String(128), comment="当前公司")
    current_position = Column(String(128), comment="当前职位")
    skills = Column(String(512), comment="核心技能")
    status = Column(String(20), default="new", comment="new/screening/interview/offer/hired/rejected")
    match_score = Column(Integer, comment="AI匹配分0-100")
    source = Column(String(64), comment="来源渠道")
    create_time = Column(DateTime, default=datetime.now)


class Interview(Base):
    """面试安排"""
    __tablename__ = "recruitment_interview"
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, comment="关联简历")
    candidate_name = Column(String(64))
    interviewer = Column(String(64), comment="面试官")
    interview_time = Column(DateTime, comment="面试时间")
    location = Column(String(128), comment="面试地点/会议链接")
    feedback = Column(Text, comment="面试评价")
    result = Column(String(20), comment="pending/pass/fail")
    create_time = Column(DateTime, default=datetime.now)


class Offer(Base):
    """Offer记录"""
    __tablename__ = "recruitment_offer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer)
    candidate_name = Column(String(64))
    position = Column(String(128))
    salary = Column(Numeric(10, 2), comment="offer薪资")
    entry_date = Column(Date, comment="预计入职日")
    status = Column(String(20), default="sent", comment="sent/accepted/rejected")
    create_time = Column(DateTime, default=datetime.now)
