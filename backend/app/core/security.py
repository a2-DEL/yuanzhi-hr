"""安全工具：JWT、密码哈希、API Key加解密"""
from datetime import datetime, timedelta, UTC
from jose import jwt
import bcrypt
from cryptography.fernet import Fernet
import base64
from app.config import settings


# ===== 密码哈希（直接使用bcrypt，避免passlib兼容问题） =====
def hash_password(password: str) -> str:
    pwd = password.encode("utf-8")
    # bcrypt限制72字节，超长截断
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(pwd[:72], salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8"))
    except Exception:
        return False


# ===== JWT =====
def create_access_token(subject: str, extra: dict = None) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


# ===== API Key 加密存储 =====
def _get_fernet() -> Fernet:
    key = base64.urlsafe_b64encode(settings.ENCRYPT_KEY.encode().ljust(32)[:32])
    return Fernet(key)


def encrypt_api_key(plain_key: str) -> str:
    return _get_fernet().encrypt(plain_key.encode()).decode()


def decrypt_api_key(encrypted: str) -> str:
    return _get_fernet().decrypt(encrypted.encode()).decode()
