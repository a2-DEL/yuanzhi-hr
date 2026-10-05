"""系统管理数据模型：用户、角色、权限"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text, SmallInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


# 用户-角色 多对多关联表
user_role = Table(
    "sys_user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("sys_user.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("sys_role.id", ondelete="CASCADE"), primary_key=True),
)


class Role(Base):
    """角色表"""
    __tablename__ = "sys_role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_code = Column(String(64), unique=True, nullable=False, comment="角色编码")
    role_name = Column(String(64), nullable=False, comment="角色名称")
    role_level = Column(String(32), comment="角色层级：决策层/管理层/执行层/员工层/运维层/协作层")
    role_desc = Column(String(255), comment="角色描述")
    is_builtin = Column(SmallInteger, default=0, comment="是否内置角色")
    data_scope = Column(String(32), default="self", comment="数据范围：all/dept_and_child/dept/self/custom")
    sort = Column(Integer, default=0)
    status = Column(SmallInteger, default=1, comment="0禁用 1启用")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    users = relationship("User", secondary=user_role, back_populates="roles")


class User(Base):
    """用户表"""
    __tablename__ = "sys_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, comment="登录账号")
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(64), nullable=False, comment="真实姓名")
    email = Column(String(128))
    phone = Column(String(20))
    avatar = Column(String(255))
    dept_id = Column(Integer, ForeignKey("org_department.id"), nullable=True, comment="所属部门")
    position = Column(String(64), comment="岗位")
    is_superuser = Column(SmallInteger, default=0, comment="是否超级管理员")
    status = Column(SmallInteger, default=1, comment="0禁用 1启用")
    last_login = Column(DateTime)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    roles = relationship("Role", secondary=user_role, back_populates="users", lazy="joined")
    department = relationship("Department", foreign_keys=[dept_id], lazy="joined")


class OperationLog(Base):
    """操作审计日志"""
    __tablename__ = "sys_operation_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, comment="操作人ID")
    user_name = Column(String(64), comment="操作人姓名")
    module = Column(String(64), comment="操作模块")
    action = Column(String(64), comment="操作类型")
    detail = Column(Text, comment="操作详情")
    ip = Column(String(64))
    create_time = Column(DateTime, default=datetime.now)
