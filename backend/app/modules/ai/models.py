"""AI模型配置与调用记录数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, Numeric
from datetime import datetime
from app.core.database import Base


class AIModelConfig(Base):
    """用户自配置的AI模型厂商与密钥"""
    __tablename__ = "ai_model_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String(64), nullable=False, comment="厂商：openai/doubao/deepseek/qwen/zhipu/moonshot/custom")
    provider_name = Column(String(128), comment="厂商显示名")
    base_url = Column(String(512), nullable=False, comment="API基础地址")
    api_key_encrypted = Column(Text, nullable=False, comment="加密存储的API Key")
    default_model = Column(String(128), comment="默认模型名")
    # 路由优先级：high高精度/normal常规/low低成本
    route_level = Column(String(32), default="normal", comment="路由等级")
    is_enabled = Column(SmallInteger, default=1, comment="是否启用")
    is_default = Column(SmallInteger, default=0, comment="是否为默认")
    # 单价（用于成本估算）
    price_per_1k_input = Column(Numeric(10, 4), default=0)
    price_per_1k_output = Column(Numeric(10, 4), default=0)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class AIUsageLog(Base):
    """AI调用日志与成本统计"""
    __tablename__ = "ai_usage_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String(64))
    model = Column(String(128))
    agent_code = Column(String(64), comment="调用Agent编码")
    scene = Column(String(128), comment="业务场景")
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    cost_estimate = Column(Numeric(10, 6), default=0, comment="预估费用")
    status = Column(String(32), comment="success/failed")
    error_msg = Column(Text)
    create_time = Column(DateTime, default=datetime.now)
