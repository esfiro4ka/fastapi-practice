from fastapi import FastAPI
from .routers import authentication, protected_resource

app = FastAPI()

app.include_router(authentication.router)
app.include_router(protected_resource.router)
