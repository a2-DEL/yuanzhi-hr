"""员工关系管理模块数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, Date
from datetime import datetime
from app.core.database import Base


class LaborContract(Base):
    """劳动合同"""
    __tablename__ = "er_labor_contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer)
    employee_name = Column(String(64))
    contract_type = Column(String(32), comment="固定期限/无固定期限/实习")
    start_date = Column(Date)
    end_date = Column(Date, comment="NULL表示无固定期限")
    sign_date = Column(Date, comment="签订日期")
    status = Column(String(20), default="active", comment="active/expiring/expired/terminated")
    create_time = Column(DateTime, default=datetime.now)


class EmployeeTransfer(Base):
    """入转调离记录"""
    __tablename__ = "er_transfer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(64))
    change_type = Column(String(20), comment="入职/转正/调岗/晋升/离职")
    from_dept = Column(String(128), comment="原部门")
    to_dept = Column(String(128), comment="新部门")
    from_position = Column(String(128))
    to_position = Column(String(128))
    effective_date = Column(Date)
    reason = Column(Text)
    create_time = Column(DateTime, default=datetime.now)


class Discipline(Base):
    """奖惩记录"""
    __tablename__ = "er_discipline"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(64))
    type = Column(String(20), comment="奖励/警告/记过/开除")
    title = Column(String(128))
    description = Column(Text)
    occur_date = Column(Date)
    approver = Column(String(64))
    create_time = Column(DateTime, default=datetime.now)


class Offboarding(Base):
    """离职管理"""
    __tablename__ = "er_offboarding"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(64))
    dept_name = Column(String(128))
    position = Column(String(128))
    resign_date = Column(Date, comment="申请日期")
    last_day = Column(Date, comment="最后工作日")
    reason_category = Column(String(64), comment="原因分类：薪资/发展/家庭/不适应/其他")
    reason_detail = Column(Text, comment="离职面谈记录")
    status = Column(String(20), default="pending", comment="pending/in_process/completed")
    create_time = Column(DateTime, default=datetime.now)
