import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    VALID_USERNAME: str = os.getenv("VALID_USERNAME", "")
    VALID_PASSWORD: str = os.getenv("VALID_PASSWORD", "")