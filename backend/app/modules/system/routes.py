"""系统管理：认证与用户路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, hash_password
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.common.audit import log_operation
from app.modules.system.models import User, Role
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["系统认证"])


class LoginIn(BaseModel):
    username: str
    password: str


@router.post("/auth/login", summary="登录")
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise AppException(message="账号或密码错误")
    if user.status != 1:
        raise AppException(message="账号已被禁用")

    user.last_login = datetime.now()
    db.commit()
    log_operation(db, user.id, user.real_name, "认证", "登录", f"用户 {user.username} 登录成功")

    token = create_access_token(
        str(user.id),
        {"name": user.real_name, "is_super": user.is_superuser}
    )
    return success({
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "avatar": user.avatar,
            "is_superuser": user.is_superuser,
            "roles": [r.role_code for r in user.roles],
            "dept_id": user.dept_id,
        }
    }, "登录成功")


@router.get("/auth/me", summary="当前用户信息")
def me(user: User = Depends(get_current_user)):
    return success({
        "id": user.id,
        "username": user.username,
        "real_name": user.real_name,
        "email": user.email,
        "phone": user.phone,
        "avatar": user.avatar,
        "position": user.position,
        "dept_id": user.dept_id,
        "dept_name": user.department.dept_name if user.department else None,
        "is_superuser": user.is_superuser,
        "roles": [{"code": r.role_code, "name": r.role_name} for r in user.roles],
    })


@router.get("/system/users", summary="用户列表")
def user_list(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    users = db.query(User).all()
    return success([{
        "id": u.id, "username": u.username, "real_name": u.real_name,
        "email": u.email, "phone": u.phone, "position": u.position,
        "dept_id": u.dept_id, "status": u.status,
        "roles": [r.role_code for r in u.roles],
        "create_time": u.create_time.strftime("%Y-%m-%d %H:%M") if u.create_time else None,
    } for u in users])


class UserCreate(BaseModel):
    username: str
    password: str
    real_name: str
    email: str = None
    phone: str = None
    dept_id: int = None
    position: str = None


@router.post("/system/users", summary="创建用户")
def create_user(body: UserCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if db.query(User).filter(User.username == body.username).first():
        raise AppException(message="账号已存在")
    u = User(
        username=body.username,
        password_hash=hash_password(body.password),
        real_name=body.real_name,
        email=body.email, phone=body.phone,
        dept_id=body.dept_id, position=body.position,
    )
    db.add(u)
    db.commit()
    return success(msg="创建成功")


@router.get("/system/roles", summary="角色列表")
def role_list(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    roles = db.query(Role).order_by(Role.sort).all()
    return success([{
        "id": r.id, "code": r.role_code, "name": r.role_name,
        "level": r.role_level, "desc": r.role_desc,
        "data_scope": r.data_scope, "status": r.status,
    } for r in roles])
