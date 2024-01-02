from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from .config import ALGORITHM, SECRET_KEY
from ..routers.authentication import ROLE_PERMISSIONS

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    if token is None:
        user_info = {
            "role": "guest",
            "permissions": ROLE_PERMISSIONS["guest"],
        }
        return user_info
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_info = {
            "sub": payload.get("sub"),
            "role": payload.get("role"),
            "permissions": payload.get("permissions"),
        }
        return user_info
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def check_permisson(permission):
    def check(user_info: dict = Depends(get_user_from_token)):
        if permission not in user_info["permissions"]:
            raise HTTPException(
                status_code=403,
                detail="Wrong permissions."
            )
        return user_info
    return check
