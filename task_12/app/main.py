from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from . import router
from .db import database, create_table, NotFoundException


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await create_table()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(router.router)


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(
    request: Request, exc: NotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"message": exc.detail},
    )
