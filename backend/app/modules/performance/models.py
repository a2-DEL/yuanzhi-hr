"""绩效管理模块数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, Numeric
from datetime import datetime
from app.core.database import Base


class KpiIndicator(Base):
    """KPI指标库"""
    __tablename__ = "performance_kpi_indicator"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, comment="指标名称")
    department = Column(String(64), comment="适用部门")
    weight = Column(Numeric(5, 2), default=0, comment="权重%")
    target = Column(String(255), comment="考核目标/标准")
    calculation = Column(String(255), comment="计算方式")
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, default=datetime.now)


class PerformanceCycle(Base):
    """考核周期"""
    __tablename__ = "performance_cycle"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, comment="如 2026年Q3")
    type = Column(String(20), comment="monthly/quarterly/yearly")
    start_date = Column(String(20))
    end_date = Column(String(20))
    status = Column(String(20), default="draft", comment="draft/ongoing/completed")
    create_time = Column(DateTime, default=datetime.now)


class PerformanceScore(Base):
    """员工绩效评分"""
    __tablename__ = "performance_score"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cycle_id = Column(Integer, comment="考核周期")
    employee_id = Column(Integer)
    employee_name = Column(String(64))
    dept_name = Column(String(128))
    self_score = Column(Numeric(5, 2), comment="自评分")
    manager_score = Column(Numeric(5, 2), comment="上级评分")
    final_score = Column(Numeric(5, 2), comment="最终得分")
    grade = Column(String(10), comment="S/A/B/C/D")
    comment = Column(Text, comment="评语/改进建议")
    status = Column(String(20), default="pending", comment="pending/self_done/manager_done/submitted")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
