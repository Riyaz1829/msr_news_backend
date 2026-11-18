import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing from .env")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")