"""数据备份路由"""
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
import shutil
import os
from datetime import datetime
from app.core.response import success
from app.core.deps import get_current_user

router = APIRouter(prefix="/api/backup", tags=["数据备份"])

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "yuanzhi_hr.db")
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "backups")


@router.post("/create", summary="创建备份")
def create_backup(_=Depends(get_current_user)):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{ts}.db")
    shutil.copy2(DB_PATH, backup_path)
    return success({"file": f"backup_{ts}.db"}, message="备份成功")


@router.get("/list", summary="备份列表")
def list_backups(_=Depends(get_current_user)):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    files = sorted(os.listdir(BACKUP_DIR), reverse=True)
    return success([{"file": f, "size": os.path.getsize(os.path.join(BACKUP_DIR, f))} for f in files if f.endswith(".db")])


@router.get("/download/{filename}", summary="下载备份")
def download_backup(filename: str, _=Depends(get_current_user)):
    path = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path, filename=filename)
    return success({}, message="文件不存在")
