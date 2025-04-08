import os
from dotenv import load_dotenv

class Config:
    """
    Configuration settings for the postgres database.
    """
    # Load environment variables from .env file
    load_dotenv()

    # API Configuration
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

    # Database Configuration
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"