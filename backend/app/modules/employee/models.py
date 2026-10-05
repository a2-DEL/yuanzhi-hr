"""员工档案数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, SmallInteger, Text
from datetime import datetime
from app.core.database import Base


class Employee(Base):
    __tablename__ = "hr_employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    emp_no = Column(String(32), unique=True, comment="工号")
    name = Column(String(64), nullable=False, comment="姓名")
    gender = Column(SmallInteger, comment="1男 2女")
    birthday = Column(Date)
    id_card = Column(String(18), comment="身份证")
    phone = Column(String(20))
    email = Column(String(128))
    dept_id = Column(Integer, comment="部门ID")
    position = Column(String(64), comment="岗位")
    employee_type = Column(String(32), comment="正式/实习/劳务派遣")
    entry_date = Column(Date, comment="入职日期")
    regular_date = Column(Date, comment="转正日期")
    leave_date = Column(Date, comment="离职日期")
    status = Column(String(32), default="active", comment="active/probation/left")
    # 合同与试用期
    contract_start = Column(Date, comment="合同开始日")
    contract_end = Column(Date, comment="合同到期日")
    # 教育背景
    education = Column(String(32), comment="学历：大专/本科/硕士/博士")
    graduation_school = Column(String(128), comment="毕业院校")
    major = Column(String(64), comment="专业")
    # 联系方式
    emergency_contact = Column(String(64), comment="紧急联系人")
    emergency_phone = Column(String(20), comment="紧急联系电话")
    bank_account = Column(String(32), comment="工资银行卡号")
    # 薪资字段（脱敏存储，普通角色不可见）
    base_salary = Column(Numeric(10, 2), comment="基本工资")
    # 关联登录账号
    user_id = Column(Integer, comment="关联系统用户ID")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
