"""操作审计日志工具"""
from sqlalchemy.orm import Session
from app.modules.system.models import OperationLog


def log_operation(db: Session, user_id: int, user_name: str,
                  module: str, action: str, detail: str = "", ip: str = ""):
    """记录操作日志"""
    try:
        log = OperationLog(
            user_id=user_id, user_name=user_name,
            module=module, action=action, detail=detail, ip=ip
        )
        db.add(log)
        db.commit()
    except Exception:
        db.rollback()
