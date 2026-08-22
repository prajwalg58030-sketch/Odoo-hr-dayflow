#app/config/mail.py

import os
from dotenv import load_dotenv

load_dotenv()

class MailConfig:
    MAIL_SERVER = os.getenv('MAIL_HOST', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', 'noreply@dayflow.com')
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5500')