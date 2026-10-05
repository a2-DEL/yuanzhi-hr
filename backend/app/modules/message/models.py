"""站内消息模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from app.core.database import Base


class Message(Base):
    __tablename__ = "sys_message"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    msg_type = Column(String(20), default="system")  # system/approval/warning/birthday
    target_user_id = Column(Integer, index=True)  # 接收人，0=全员
    is_read = Column(Boolean, default=False)
    create_time = Column(DateTime, default=datetime.now)
