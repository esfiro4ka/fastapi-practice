import os

from dotenv import load_dotenv
from passlib.context import CryptContext


load_dotenv()

SECRET_KEY = os.environ.get("MY_APP_SECRET_KEY")
ALGORITHM = "HS256"

crypt_ctx = CryptContext(schemes=['bcrypt'])
