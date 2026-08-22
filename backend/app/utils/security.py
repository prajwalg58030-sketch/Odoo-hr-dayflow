import bcrypt
import secrets
import string
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False

def generate_temp_password(length=12):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password) 
            and any(c.isupper() for c in password) 
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%^&*" for c in password)):
            return password

def generate_verification_token():
    return secrets.token_urlsafe(32)

def generate_login_id(first_name, last_name, joining_year, serial):
    fn = ''.join(c for c in first_name.upper() if c.isalpha())[:2]
    ln = ''.join(c for c in last_name.upper() if c.isalpha())[:2]
    return f"OI{fn}{ln}{joining_year}{serial:04d}"