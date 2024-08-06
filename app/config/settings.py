from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    USER: str = os.getenv('USER')
    PASSWORD: str = os.getenv('PASSWORD')
    HOST: str = os.getenv('HOST')
    PORT: int = os.getenv('PORT')
    DB: str = os.getenv('DB_NAME')
    DATABASE_URL: str = Field(default=f"db+postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

    JWT_SECRET: str = os.getenv('secret')
    JWT_ALGORITHM: str = os.getenv('algorithm')

    
settings = Settings()

