"""数据库连接与会话管理"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import os

# SQLite需要确保目录存在
if settings.database_url.startswith("sqlite"):
    db_path = settings.SQLITE_PATH
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    settings.database_url,
    echo=settings.APP_DEBUG,
    connect_args={"check_same_thread": False} if settings.DB_TYPE == "sqlite" else {},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表"""
    # 导入所有模型以注册到Base
    from app.modules.system import models  # noqa
    from app.modules.organization import models  # noqa
    from app.modules.employee import models  # noqa
    from app.modules.attendance import models  # noqa
    from app.modules.salary import models  # noqa
    from app.modules.planning import models  # noqa
    from app.modules.recruitment import models  # noqa
    from app.modules.training import models  # noqa
    from app.modules.performance import models  # noqa
    from app.modules.employee_relation import models  # noqa
    from app.modules.ai import models  # noqa
    Base.metadata.create_all(bind=engine)
