"""审批流路由"""
from fastapi import APIRouter, Depends
from app.core.response import success
from app.core.deps import get_current_user
from app.core.database import SessionLocal
from app.modules.approval.models import ApprovalFlow, ApprovalInstance
import json

router = APIRouter(prefix="/api/approval", tags=["审批流"])


@router.get("/flows", summary="审批流列表")
def list_flows(_=Depends(get_current_user)):
    db = SessionLocal()
    flows = db.query(ApprovalFlow).all()
    db.close()
    return success([{
        "id": f.id, "flow_name": f.flow_name, "flow_type": f.flow_type,
        "nodes": json.loads(f.nodes) if f.nodes else [],
        "status": f.status,
    } for f in flows])


@router.get("/pending", summary="待我审批")
def my_pending(user=Depends(get_current_user)):
    db = SessionLocal()
    instances = db.query(ApprovalInstance).filter(
        ApprovalInstance.status == "pending"
    ).order_by(ApprovalInstance.create_time.desc()).all()
    db.close()
    return success([{
        "id": i.id, "biz_type": i.biz_type, "biz_id": i.biz_id,
        "applicant_id": i.applicant_id, "current_node": i.current_node,
        "status": i.status, "time": i.create_time.strftime("%Y-%m-%d %H:%M"),
    } for i in instances])


@router.post("/approve/{instance_id}", summary="审批通过")
def approve(instance_id: int, _=Depends(get_current_user)):
    db = SessionLocal()
    inst = db.query(ApprovalInstance).filter(ApprovalInstance.id == instance_id).first()
    if inst:
        inst.status = "approved"
        db.commit()
    db.close()
    return success({}, message="已审批通过")


@router.post("/reject/{instance_id}", summary="审批驳回")
def reject(instance_id: int, _=Depends(get_current_user)):
    db = SessionLocal()
    inst = db.query(ApprovalInstance).filter(ApprovalInstance.id == instance_id).first()
    if inst:
        inst.status = "rejected"
        db.commit()
    db.close()
    return success({}, message="已驳回")
