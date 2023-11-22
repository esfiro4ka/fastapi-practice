from fastapi import FastAPI
from .models.models import User, Feedback


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


feedback_list = []


@app.post("/feedback")
async def feedback(feedback: Feedback):
    feedback_list.append({"name": feedback.name, "message": feedback.message})
    return {
        "message": f"Feedback received. Thank you, {feedback.name}!"
    }


@app.get("/reviews")
async def show_feedback_list():
    return feedback_list
