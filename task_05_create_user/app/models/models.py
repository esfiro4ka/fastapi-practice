from typing import Union
from pydantic import BaseModel, EmailStr, conint


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: conint(ge=0, le=150)
    is_subscribed: Union[bool, None] = None
