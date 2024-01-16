from fastapi import APIRouter

from .db import database, get_existing_task
from .models import Task, TaskCreate, TaskUpdate


router = APIRouter()


@router.post("/tasks/", response_model=Task)
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


@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int):
    existing_task = await get_existing_task(task_id)
    return dict(existing_task)


@router.put("/tasks/{task_id}/update", response_model=Task)
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


@router.delete("/tasks/{task_id}/delete")
async def delete_task(task_id: int):
    await get_existing_task(task_id)
    query = """DELETE FROM tasks WHERE id = :id"""
    await database.fetch_one(query, values={"id": task_id})
    return {"message": "Task successfully deleted"}
