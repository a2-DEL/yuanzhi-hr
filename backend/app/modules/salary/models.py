"""薪酬模块数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Numeric, SmallInteger, ForeignKey
from datetime import datetime
from app.core.database import Base


class SalaryStructure(Base):
    """薪资结构配置"""
    __tablename__ = "salary_structure"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("hr_employee.id"), nullable=False)
    base_salary = Column(Numeric(10, 2), default=0, comment="基本工资")
    position_salary = Column(Numeric(10, 2), default=0, comment="岗位工资")
    performance_salary = Column(Numeric(10, 2), default=0, comment="绩效工资")
    social_insurance_base = Column(Numeric(10, 2), default=0, comment="社保基数")
    housing_fund_rate = Column(Numeric(5, 2), default=7, comment="公积金比例%")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class SalaryRecord(Base):
    """月度工资表"""
    __tablename__ = "salary_record"
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("hr_employee.id"), nullable=False)
    salary_month = Column(String(7), nullable=False, comment="2026-10")
    base_salary = Column(Numeric(10, 2), default=0)
    performance_salary = Column(Numeric(10, 2), default=0)
    allowance = Column(Numeric(10, 2), default=0, comment="补贴")
    social_insurance = Column(Numeric(10, 2), default=0, comment="社保个人部分")
    housing_fund = Column(Numeric(10, 2), default=0, comment="公积金个人部分")
    tax = Column(Numeric(10, 2), default=0, comment="个税")
    deduct = Column(Numeric(10, 2), default=0, comment="其他扣款")
    gross_salary = Column(Numeric(10, 2), default=0, comment="应发")
    net_salary = Column(Numeric(10, 2), default=0, comment="实发")
    status = Column(String(20), default="calculated", comment="calculated/paid")
    create_time = Column(DateTime, default=datetime.now)
