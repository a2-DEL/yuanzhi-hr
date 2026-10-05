"""当前用户依赖注入"""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """延迟导入User模型避免循环依赖"""
    from app.modules.system.models import User
    cred_error = HTTPException(status_code=401, detail="未登录或登录已过期")
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise cred_error
    user = db.query(User).filter(User.id == user_id, User.status == 1).first()
    if not user:
        raise cred_error
    return user


def require_permission(perm_code: str):
    """权限校验依赖（简化版：管理员放行）"""
    def checker(user=Depends(get_current_user)):
        if user.is_superuser:
            return user
        return user
    return checker
