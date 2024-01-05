from databases import Database
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .models.models import Task, TaskCreate

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
