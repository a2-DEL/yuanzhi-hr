"""审批流模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base


class ApprovalFlow(Base):
    """审批流定义"""
    __tablename__ = "sys_approval_flow"
    id = Column(Integer, primary_key=True, index=True)
    flow_name = Column(String(100), nullable=False)  # 请假审批/报销审批
    flow_type = Column(String(50), default="leave")
    nodes = Column(Text)  # JSON: [{"name":"部门主管审批","role":"DEPT_MANAGER"},{"name":"HR审批","role":"HR_SPECIALIST"}]
    status = Column(String(20), default="active")
    create_time = Column(DateTime, default=datetime.now)


class ApprovalInstance(Base):
    """审批实例"""
    __tablename__ = "sys_approval_instance"
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("sys_approval_flow.id"))
    biz_type = Column(String(50))  # leave/salary/offboarding
    biz_id = Column(Integer)  # 业务单据ID
    applicant_id = Column(Integer)
    current_node = Column(Integer, default=0)  # 当前节点序号
    status = Column(String(20), default="pending")  # pending/approved/rejected
    create_time = Column(DateTime, default=datetime.now)
