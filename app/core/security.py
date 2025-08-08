from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_token(subject: str, expires_delta_minutes: int, secret_key: str, token_type: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta_minutes)
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "type": token_type,
        "iat": datetime.now(timezone.utc).timestamp(),
    }
    return jwt.encode(payload, secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str) -> str:
    return create_token(
        subject=subject,
        expires_delta_minutes=settings.access_token_expire_minutes,
        secret_key=settings.jwt_secret_key,
        token_type="access",
    )


def create_refresh_token(subject: str) -> str:
    return create_token(
        subject=subject,
        expires_delta_minutes=settings.refresh_token_expire_minutes,
        secret_key=settings.jwt_refresh_secret_key,
        token_type="refresh",
    )


def decode_token(token: str, secret_key: str) -> Optional[dict[str, Any]]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None