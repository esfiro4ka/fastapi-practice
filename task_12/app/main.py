from databases import Database
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from .models.models import Task, TaskCreate, TaskUpdate

DATABASE_URL = "postgresql+asyncpg://admin:password@localhost:5432/dbname"

database = Database(DATABASE_URL)


async def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id serial PRIMARY KEY,
        title TEXT,
        description TEXT,
        completed BOOLEAN DEFAULT FALSE
    )
    """
    await database.execute(query)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await create_table()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    query = """
    INSERT INTO tasks (
        title,
        description
    ) VALUES (:title, :description)
    RETURNING *
    """
    data = await database.fetch_one(query, values=dict(task))
    return dict(data)


async def get_existing_task(task_id: int):
    query = "SELECT * FROM tasks WHERE id = :id"
    existing_task = await database.fetch_one(query, values={"id": task_id})
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return existing_task


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    existing_task = await get_existing_task(task_id)
    return dict(existing_task)


@app.put("/tasks/{task_id}/update", response_model=Task)
async def update_task(task_id: int, task: TaskUpdate):
    await get_existing_task(task_id)
    query = """
    UPDATE tasks
    SET title = :title,
        description = :description,
        completed = :completed
    WHERE id = :id
    RETURNING *
    """
    data = await database.fetch_one(query, values=dict(task, id=task_id))
    return dict(data)


@app.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int):
    await get_existing_task(task_id)
    query = """DELETE FROM tasks WHERE id = :id"""
    await database.fetch_one(query, values={"id": task_id})
    return {"message": "Task succesfully delete"}
