"""站内消息路由"""
from fastapi import APIRouter, Depends
from app.core.response import success
from app.core.deps import get_current_user
from app.core.database import SessionLocal
from app.modules.message.models import Message

router = APIRouter(prefix="/api/message", tags=["站内消息"])


@router.get("/list", summary="我的消息列表")
def my_messages(user=Depends(get_current_user)):
    db = SessionLocal()
    msgs = db.query(Message).filter(
        (Message.target_user_id == user.id) | (Message.target_user_id == 0)
    ).order_by(Message.create_time.desc()).limit(50).all()
    db.close()
    return success([{
        "id": m.id, "title": m.title, "content": m.content,
        "type": m.msg_type, "is_read": m.is_read,
        "time": m.create_time.strftime("%Y-%m-%d %H:%M"),
    } for m in msgs])


@router.get("/unread", summary="未读消息数")
def unread_count(user=Depends(get_current_user)):
    db = SessionLocal()
    count = db.query(Message).filter(
        (Message.target_user_id == user.id) | (Message.target_user_id == 0),
        Message.is_read == False
    ).count()
    db.close()
    return success({"count": count})


@router.post("/read/{msg_id}", summary="标记已读")
def mark_read(msg_id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    msg = db.query(Message).filter(Message.id == msg_id).first()
    if msg:
        msg.is_read = True
        db.commit()
    db.close()
    return success({}, message="已标记")


def send_message(title: str, content: str, msg_type: str = "system", target_user_id: int = 0):
    """工具函数：发送消息"""
    db = SessionLocal()
    db.add(Message(title=title, content=content, msg_type=msg_type, target_user_id=target_user_id))
    db.commit()
    db.close()
