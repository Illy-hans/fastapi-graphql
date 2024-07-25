import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # PROJECT_TITLE: str = "Fast Api GraphQL Strawberry"
    # PROJECT_VERSION: str = "0.0.1"
    # HOST_HTTP: str = os.environ.get("HOST_HTTP","http://")
    # HOST_URL: str = os.environ.get("HOST_URL")
    # HOST_PORT: int = int(os.environ.get("HOST_PORT"))
    # BASE_URL: str = HOST_HTTP+HOST_URL+":"+str(HOST_PORT)
    USER: str = os.environ.get("USER",)
    PASSWORD: str = os.environ.get("PASSWORD")
    HOST: str = os.environ.get("HOST")
    PORT: int = int(os.environ.get("PORT", 5432))
    DB: str = os.environ.get("DB_NAME")
    DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
        
settings = Settings()

