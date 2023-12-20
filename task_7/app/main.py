from fastapi import FastAPI, Response, Cookie
from .models.models import User
from typing import Optional
import uuid


app = FastAPI()

sample_users = [
    {"username": "user1", "password": "password123", "session_token": None},
    {"username": "user2", "password": "password456", "session_token": None},
    {"username": "user3", "password": "password789", "session_token": None},
]


def generate_session_token():
    return str(uuid.uuid4())


@app.post("/login")
async def login_user(current_user: User, response: Response):
    for user in sample_users:
        if (user["username"] == current_user.username and
           user["password"] == current_user.password):
            session_token = generate_session_token()
            user["session_token"] = session_token
            response.set_cookie(
                key="session_token", value=session_token, httponly=True
            )
            return {"message": "Cookie установлены"}
    return {"message": "Неверные username или password"}


# Postman: Cookies -> Manage cookies
@app.get("/user")
async def user_info(session_token: Optional[str] = Cookie(None)):
    if session_token is None:
        return {"message": "Пользователь неавторизован"}
    for user in sample_users:
        if user["session_token"] == session_token:
            return user
    return {"message": "Пользователь неавторизован"}
