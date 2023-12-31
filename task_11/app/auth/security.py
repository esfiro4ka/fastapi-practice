from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from .config import ALGORITHM, SECRET_KEY
from ..db.db import get_user


crypt_ctx = CryptContext(schemes=['bcrypt'])

expiration_time = datetime.utcnow() + timedelta(hours=24)


def get_authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not crypt_ctx.verify(password, user["password"]):
        return None
    return user


def create_jwt_token(data: dict, expiration_time: datetime):
    data_to_encode = data.copy()
    data_to_encode["exp"] = expiration_time
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
