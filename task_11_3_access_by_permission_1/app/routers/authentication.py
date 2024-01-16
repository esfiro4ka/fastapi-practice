from datetime import datetime, timedelta
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from ..models.models import User
from ..auth.security import (create_jwt_token, get_authenticate_user)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

ROLE_PERMISSIONS = {"admin": {"read", "create", "update", "delete"},
                    "user": {"read", "update"},
                    "guest": {"read"}}


@router.post("/login")
async def login(user_in: User):
    user = get_authenticate_user(user_in.username, user_in.password)
    if user:
        role = user.get("role")
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        return {
            "access_token": create_jwt_token(
                {"sub": user_in.username,
                 "role": role,
                 "permissions": ROLE_PERMISSIONS[role]},
                expiration_time
            ),
            "token_type": "bearer"
        }
    return {"error": "Invalid credentials"}
