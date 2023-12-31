import os

from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.environ.get("MY_APP_SECRET_KEY")
ALGORITHM = "HS256"
