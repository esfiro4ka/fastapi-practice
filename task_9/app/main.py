from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .models.models import User

app = FastAPI()
security = HTTPBasic()


USER_DATA = [
    User(**{"username": "user1", "password": "123"}),
    User(**{"username": "user2", "password": "456"})]


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


# Authorization: Basic Auth (Username, Password)
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"})
    return user


@app.get("/login")
def get_login(user: User = Depends(authenticate_user)):
    return {"message": "You got my secret, welcome",
            "user_info": user}
