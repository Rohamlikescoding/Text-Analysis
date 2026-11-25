import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SECRET_KEY = os.environ["SECRET_KEY"]     
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60