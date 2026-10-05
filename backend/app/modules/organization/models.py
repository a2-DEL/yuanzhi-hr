"""组织架构数据模型：部门"""
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from datetime import datetime
from app.core.database import Base


class Department(Base):
    __tablename__ = "org_department"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, default=0, comment="父级ID，0为根节点")
    dept_name = Column(String(128), nullable=False, comment="部门名称")
    dept_code = Column(String(64), comment="部门编码")
    manager_id = Column(Integer, comment="部门负责人用户ID")
    sort = Column(Integer, default=0)
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Position(Base):
    __tablename__ = "org_position"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dept_id = Column(Integer, comment="所属部门")
    position_name = Column(String(128), comment="岗位名称")
    position_code = Column(String(64))
    job_description = Column(String(1000), comment="岗位说明书")
    headcount = Column(Integer, default=1, comment="编制人数")
    sort = Column(Integer, default=0)
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, default=datetime.now)
