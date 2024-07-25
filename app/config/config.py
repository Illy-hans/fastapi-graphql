import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    USER: str = os.environ.get("USER",)
    PASSWORD: str = os.environ.get("PASSWORD")
    HOST: str = os.environ.get("HOST")
    PORT: int = int(os.environ.get("PORT", 5432))
    DB: str = os.environ.get("DB_NAME")
    DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
        
settings = Settings()

