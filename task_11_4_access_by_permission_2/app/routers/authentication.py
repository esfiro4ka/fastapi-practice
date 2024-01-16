from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from ..models.models import User
from ..auth.security import (create_jwt_token, get_authenticate_user)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
async def login(user_in: User):
    user = get_authenticate_user(user_in.username, user_in.password)
    if user:
        role = user.role
        permissions = user.permissions
        expiration_time = datetime.utcnow() + timedelta(hours=24)
        return {
            "access_token": create_jwt_token(
                {"sub": user_in.username,
                 "role": str(role),
                 "permissions": str(permissions)},
                expiration_time
            ),
            "token_type": "bearer"
        }
    return {"error": "Invalid credentials"}
