from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    # для второго варианта:
    # is_adult: bool = False
