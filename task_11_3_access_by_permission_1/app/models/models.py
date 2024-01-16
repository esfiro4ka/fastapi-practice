from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Role(Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class User(BaseModel):
    username: str
    password: str
    role: Optional[Role] = None
