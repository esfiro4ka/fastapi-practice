from datetime import datetime
import jwt
from .config import ALGORITHM, SECRET_KEY
from ..db.db import get_user
from passlib.context import CryptContext

crypt_ctx = CryptContext(schemes=['bcrypt'])


def get_authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not crypt_ctx.verify(password, user["password"]):
        return None
    return user


def create_jwt_token(data: dict, expiration_time: datetime):
    data_to_encode = data.copy()
    data_to_encode["exp"] = expiration_time
    data_to_encode["permissions"] = list(data_to_encode["permissions"])
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
