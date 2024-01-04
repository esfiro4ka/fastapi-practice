from pydantic import BaseModel
from enum import Enum
from typing import Optional
from typing import Set


class Permission(Enum):
    read = "read"
    create = "create"
    update = "update"
    delete = "delete"


class Role(Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class User(BaseModel):
    username: str
    password: str
    role: Optional[Role] = None
    permissions: Set[Permission] = set()

    @classmethod
    def create_user(cls, username: str, password: str, role: str):
        user_data = {
            "username": username, "password": password, "role": Role(role)}
        user = cls(**user_data)
        user.set_permissions_by_role()
        return user

    def set_permissions_by_role(self):
        if self.role == Role.admin:
            self.permissions = {
                Permission.read,
                Permission.create,
                Permission.update,
                Permission.delete}
        elif self.role == Role.user:
            self.permissions = {Permission.read, Permission.update}
        else:
            self.permissions = {Permission.read}
