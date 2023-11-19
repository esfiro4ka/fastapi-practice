from fastapi import FastAPI

app = FastAPI()


# POST-запрос в Postman на адрес http://localhost:8000/calculate?num1=2&num2=1
@app.post("/calculate")
async def read_items(
    num1: int,
    num2: int
):
    return {"result": num1 + num2}
