from fastapi import FastAPI
from .models.models import User


app = FastAPI()


# первый вариант:
@app.get("/user")
async def check_adult(user: User):
    return {
        "name": user.name,
        "age": user.age,
        "is_adult": user.age >= 18,
    }

# второй вариант:
# @app.post("/user")
# async def check_adult(user: User):
#     user.is_adult = user.age >= 18
#     return user

# третий вариант:
# @app.post("/user")
# async def add_user(user: User):
#     is_adult = user.age >= 18
#     return {**user.model_dump(), "is_adult": is_adult}
