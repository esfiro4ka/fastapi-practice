from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from .config import ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    if token is None:
        user_info = {
            "role": "guest",
        }
        return user_info
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


def check_role(allowed_roles: list[str]):
    def check(user_info: dict = Depends(get_user_from_token)):
        user_role = user_info["role"]
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions."
            )
        return user_info
    return check
