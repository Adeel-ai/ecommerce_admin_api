import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

path = os.path.abspath(os.environ.get("DOTENV_PATH", ".env"))
if os.path.exists(path):
    load_dotenv(dotenv_path=Path(__file__).parent / path)


class DBConfig(BaseSettings):
    HOST: str
    class Config:
        env_prefix = "DB_"

class Config:
    DB = DBConfig()
