from ..auth.crypt import encode_password
from ..models.models import User


USERS_DATA = [
    User.create_user(
        username="admin",
        password=encode_password("securepassword123"),
        role="admin"),
    User.create_user(
        username="user",
        password=encode_password("securepassword456"),
        role="user")
]


def get_user(username: str):
    for user in USERS_DATA:
        if user.username == username:
            return user
    return None
