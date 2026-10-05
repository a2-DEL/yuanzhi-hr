"""人力资源规划模块数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger
from datetime import datetime
from app.core.database import Base


class HeadcountBudget(Base):
    """部门编制预算"""
    __tablename__ = "planning_headcount_budget"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dept_id = Column(Integer, nullable=False, comment="部门ID")
    year = Column(Integer, nullable=False)
    budget_count = Column(Integer, default=0, comment="编制人数")
    budget_cost = Column(Integer, default=0, comment="年度人力成本预算（万元）")
    note = Column(String(255))
    create_time = Column(DateTime, default=datetime.now)


class JobDescription(Base):
    """岗位说明书"""
    __tablename__ = "planning_job_description"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False, comment="岗位名称")
    dept_id = Column(Integer, comment="所属部门")
    responsibilities = Column(Text, comment="岗位职责")
    requirements = Column(Text, comment="任职要求")
    salary_range = Column(String(64), comment="薪资范围")
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class PolicyDoc(Base):
    """HR制度文档库"""
    __tablename__ = "planning_policy_doc"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    category = Column(String(64), comment="类别：考勤/奖惩/晋升/薪酬/福利")
    content = Column(Text)
    version = Column(String(32), default="v1.0")
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, default=datetime.now)
