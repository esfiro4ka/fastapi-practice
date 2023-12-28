from ..utils.crypt import encode_password


USERS_DATA = [
    {"username": "john_doe", "password": encode_password("securepassword123")}
]


def get_user(username: str):
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None
