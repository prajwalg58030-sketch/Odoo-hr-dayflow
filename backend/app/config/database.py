#app/config/database.py


import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USERNAME', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'dayflow_db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False