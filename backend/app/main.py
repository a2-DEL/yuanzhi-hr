"""源智HR 后端主入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from app.config import settings
from app.core.database import init_db, SessionLocal
from app.core.security import hash_password
from app.core.response import app_exception_handler, validation_exception_handler, AppException
from fastapi.exceptions import RequestValidationError

# 导入路由
from app.modules.system import system_router
from app.modules.organization import org_router
from app.modules.employee import employee_router
from app.modules.ai import ai_router
from app.modules.attendance import attendance_router
from app.modules.salary import salary_router
from app.modules.planning import planning_router
from app.modules.recruitment import recruitment_router
from app.modules.training import training_router
from app.modules.performance import performance_router
from app.modules.employee_relation import employee_relation_router
from app.modules.dashboard import routes as dashboard_routes
from app.modules.plugin import routes as plugin_routes
from app.modules.self import routes as self_routes
from app.modules.export import routes as export_routes
from app.modules.message import routes as message_routes
from app.modules.approval import routes as approval_routes
from app.modules.backup import routes as backup_routes
from app.modules.memory import routes as memory_routes
from app.modules.report import routes as report_routes


def init_seed_data():
    """初始化种子数据：默认角色 + 管理员账号"""
    from app.modules.system.models import Role, User
    db = SessionLocal()
    try:
        # 预置六级角色
        default_roles = [
            ("HR_DIRECTOR", "人力经营决策者", "决策层", "all", 1),
            ("DEPT_MANAGER", "部门直线经理", "管理层", "dept_and_child", 2),
            ("HR_SPECIALIST", "HR业务专员", "执行层", "all", 3),
            ("EMPLOYEE", "普通员工", "员工层", "self", 4),
            ("ADMIN", "系统管理员", "运维层", "self", 5),
            ("EXTERNAL", "外部协作角色", "协作层", "self", 6),
        ]
        for code, name, level, scope, sort in default_roles:
            if not db.query(Role).filter(Role.role_code == code).first():
                db.add(Role(
                    role_code=code, role_name=name, role_level=level,
                    data_scope=scope, sort=sort, is_builtin=1,
                ))

        # 预置管理员账号 admin / admin123
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                real_name="系统管理员",
                is_superuser=1,
            )
            db.add(admin)
        db.commit()
        print("[初始化] 种子数据完成：默认账号 admin / admin123")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    init_db()
    init_seed_data()
    # 初始化插件发现
    from app.plugins.registry import discover_plugins
    discover_plugins()
    print(f"[启动] {settings.APP_NAME} 运行在 http://0.0.0.0:{settings.APP_PORT}")
    yield


app = FastAPI(
    title="源智HR - 基于多Agent的开源智能人力运营系统",
    description="国内首个多Agent团队驱动、用户自托管大模型、数据私有化的开源HR系统",
    version="0.1.0",
    lifespan=lifespan,
)

# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 异常处理
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 注册路由
app.include_router(system_router)
app.include_router(org_router)
app.include_router(employee_router)
app.include_router(ai_router)
app.include_router(attendance_router)
app.include_router(salary_router)
app.include_router(planning_router)
app.include_router(recruitment_router)
app.include_router(training_router)
app.include_router(performance_router)
app.include_router(employee_relation_router)
app.include_router(dashboard_routes.router)
app.include_router(plugin_routes.router)
app.include_router(self_routes.router)
app.include_router(export_routes.router)
app.include_router(message_routes.router)
app.include_router(approval_routes.router)
app.include_router(backup_routes.router)
app.include_router(memory_routes.router)
app.include_router(report_routes.router)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
        "message": "源智HR API服务已启动",
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


# 静态文件（前端构建产物）
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
