#app/config/database.py


import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
        f"postgresql+psycopg://{os.getenv('DB_USERNAME', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'dayflow_db')}"
        if os.getenv("DB_HOST")
        else "sqlite:///dayflow.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False