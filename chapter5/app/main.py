from fastapi import FastAPI, HTTPException
from typing import List
from .models.models import UserCreate


app = FastAPI()


class UserManager:
    def __init__(self):
        self.users: List[UserCreate] = []

    def create_user(self, user: UserCreate):
        if user.name in [u.name for u in self.users]:
            raise HTTPException(
                status_code=400, detail="Name already exists")
        self.users.append(user)
        return user

    def get_users(self):
        return self.users


user_manager = UserManager()


@app.post("/create_user", response_model=UserCreate)
async def create_user(user: UserCreate):
    return user_manager.create_user(user)


@app.get("/users", response_model=List[UserCreate])
async def get_users():
    return user_manager.get_users()
