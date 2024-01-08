from databases import Database


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


class NotFoundException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


async def get_existing_task(task_id: int):
    query = "SELECT * FROM tasks WHERE id = :id"
    existing_task = await database.fetch_one(query, values={"id": task_id})
    if existing_task is None:
        raise NotFoundException(detail="Task not found")
    return existing_task
