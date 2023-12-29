from pydantic import BaseModel, validator
from enum import Enum
from typing import Set


class Role(Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class Permission(Enum):
    read = "read"
    write = "write"
    update = "update"
    delete = "delete"


class User(BaseModel):
    username: str
    password: str
    role: Set[Role]
    permissions: Set[Permission] = set()

    @validator("permissions", pre=True, always=True)
    def set_permissions(cls, v, values):
        role = values.get("role")
        return cls.get_permissions_by_role(role)

    @staticmethod
    def get_permissions_by_role(role: Set[Role]) -> Set[Permission]:
        if Role.admin in role:
            return {
                Permission.read,
                Permission.write,
                Permission.update,
                Permission.delete}
        elif Role.user in role:
            return {Permission.read, Permission.update}
        else:
            return {Permission.read}
