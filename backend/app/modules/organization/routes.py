"""组织架构路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.response import success, AppException
from app.core.deps import get_current_user
from app.modules.organization.models import Department, Position
from pydantic import BaseModel

router = APIRouter(prefix="/api/org", tags=["组织架构"])


@router.get("/departments/tree", summary="部门树")
def dept_tree(db: Session = Depends(get_db), _=Depends(get_current_user)):
    depts = db.query(Department).filter(Department.status == 1).order_by(Department.sort).all()
    def build(parent_id=0):
        return [{
            "id": d.id, "label": d.dept_name, "parent_id": d.parent_id,
            "dept_code": d.dept_code, "manager_id": d.manager_id,
            "children": build(d.id)
        } for d in depts if d.parent_id == parent_id]
    return success(build())


class DeptIn(BaseModel):
    parent_id: int = 0
    dept_name: str
    dept_code: str = None
    sort: int = 0


@router.post("/departments", summary="新增部门")
def add_dept(body: DeptIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    d = Department(**body.model_dump())
    db.add(d); db.commit()
    return success(msg="部门创建成功")


@router.put("/departments/{dept_id}", summary="更新部门")
def update_dept(dept_id: int, body: DeptIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    d = db.query(Department).get(dept_id)
    if not d: raise AppException(message="部门不存在")
    for k, v in body.model_dump().items():
        setattr(d, k, v)
    db.commit()
    return success(msg="更新成功")


@router.delete("/departments/{dept_id}", summary="删除部门")
def del_dept(dept_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    d = db.query(Department).get(dept_id)
    if d:
        d.status = 0
        db.commit()
    return success(msg="删除成功")


@router.get("/positions", summary="岗位列表")
def position_list(dept_id: int = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(Position).filter(Position.status == 1)
    if dept_id: q = q.filter(Position.dept_id == dept_id)
    return success([{
        "id": p.id, "dept_id": p.dept_id, "position_name": p.position_name,
        "position_code": p.position_code, "headcount": p.headcount,
        "job_description": p.job_description,
    } for p in q.all()])
