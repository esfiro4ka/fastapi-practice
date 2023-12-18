from fastapi import FastAPI, Response
from .models.models import User


app = FastAPI()

sample_users = [
    {"username": "user1", "password": "password123", "session_token": None},
    {"username": "user2", "password": "password456", "session_token": None},
    {"username": "user3", "password": "password789", "session_token": None},
]


@app.post("/login")
async def logout_user(current_user: User, response: Response):
    for user in sample_users:
        if (user["username"] == current_user.username and
           user["password"] == current_user.password):
            session_token = "abc123xyz456"
            user["session_token"] = session_token
            response.set_cookie(
                key="session_token", value=session_token, httponly=True
            )
            return {"message": "Cookie установлены"}
    return {"message": "Неверные username или password"}
