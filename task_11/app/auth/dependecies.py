from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from .config import ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_info = {
            "sub": payload.get("sub"),
            "role": payload.get("role"),
        }
        return user_info
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def check_admin_role(user_info: dict = Depends(get_user_from_token)):
    if "admin" not in user_info["role"]:
        raise HTTPException(
            status_code=403,
            detail="Insufficient privileges. Admin role required."
        )
    return user_info
