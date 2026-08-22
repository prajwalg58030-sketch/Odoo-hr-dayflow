import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy  # 1. Import SQLAlchemy

load_dotenv()

class DatabaseConfig:
    # 10-Second Hackathon Bypass: Using local SQLite instead of Postgres
    SQLALCHEMY_DATABASE_URI = "sqlite:///dayflow.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# 2. Create the 'db' object here so all models can safely import it!
db = SQLAlchemy()