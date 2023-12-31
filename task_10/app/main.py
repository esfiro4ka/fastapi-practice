from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .models.models import User
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from passlib.context import CryptContext


load_dotenv()


app = FastAPI()

# Authorization Type: OAuth 2.0, Token: access_token, Header Prefix: Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.environ.get("MY_APP_SECRET_KEY")
ALGORITHM = "HS256"

expiration_time = datetime.utcnow() + timedelta(hours=24)

crypt_ctx = CryptContext(schemes=['bcrypt'])


def encode_password(password: str):
    return crypt_ctx.hash(password)


def verify_password(password: str, encoded_password: str):
    return crypt_ctx.verify(password, encoded_password)


USERS_DATA = [
    {"username": "john_doe", "password": encode_password("securepassword123")}
]


def get_user(username: str):
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not crypt_ctx.verify(password, user["password"]):
        return None
    return user


def create_jwt_token(data: dict, expiration_time: datetime):
    data_to_encode = data.copy()
    data_to_encode["exp"] = expiration_time
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/login")
async def login(user_in: User):
    user = authenticate_user(user_in.username, user_in.password)
    if user:
        return {
            "access_token": create_jwt_token(
                {"sub": user_in.username}, expiration_time),
            "token_type": "bearer"
        }
    return {"error": "Invalid credentials"}


@app.get("/protected_resource")
async def get_protected_resource(
    current_user: str = Depends(get_user_from_token)
):
    user = get_user(current_user)
    if user:
        return {"message": "Success"}
    return {"error": "User not found"}
