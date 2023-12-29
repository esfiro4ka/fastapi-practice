from ..auth.crypt import encode_password


USERS_DATA = [
    {"username": "admin",
     "password": encode_password("securepassword123"),
     "role": "admin"},
    {"username": "user",
     "password": encode_password("securepassword456"),
     "role": "user"},
]


def get_user(username: str):
    for user in USERS_DATA:
        if user.get("username") == username:
            return user
    return None
