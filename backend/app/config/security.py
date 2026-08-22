#app/config/security.py

import os
from dotenv import load_dotenv

load_dotenv()

class SecurityConfig:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'dev-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    BCRYPT_LOG_ROUNDS = 12