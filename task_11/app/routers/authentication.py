from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

from ..models.models import User
from ..auth.security import (create_jwt_token, get_authenticate_user,
                             expiration_time)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
async def login(user_in: User):
    user = get_authenticate_user(user_in.username, user_in.password)
    if user:
        return {
            "access_token": create_jwt_token(
                {"sub": user_in.username}, expiration_time),
            "token_type": "bearer"
        }
    return {"error": "Invalid credentials"}
