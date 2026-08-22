from datetime import datetime, timedelta
from flask import current_app
from flask_jwt_extended import create_access_token
from ..models import User, Employee
from app.config.database import db
from ..utils.security import hash_password, verify_password, generate_temp_password, generate_verification_token, generate_login_id
from ..utils.validators import validate_email
from ..errors.exceptions import APIError
from .email_service import EmailService

class AuthService:

    @staticmethod
    def register_company(data):
        company_name = data.get('company_name')
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        logo = data.get('logo')

        if not company_name or not name or not email or not password:
            raise APIError("All fields are required", "VALIDATION_ERROR", 400)
        if not validate_email(email):
            raise APIError("Invalid email format", "INVALID_EMAIL", 400)
        if len(password) < 8:
            raise APIError("Password must be at least 8 characters", "WEAK_PASSWORD", 400)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise APIError("Email already registered", "EMAIL_EXISTS", 409)

        # Create HR user
        user = User(
            email=email,
            password_hash=hash_password(password),
            role='HR',
            email_verified=False,
            must_change_password=False
        )
        db.session.add(user)
        db.session.flush()

        # Generate verification token
        token = generate_verification_token()
        verification = EmailVerificationToken(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db.session.add(verification)
        db.session.commit()

        # Send verification email (in production)
        EmailService.send_verification_email(email, token)

        return {"user_id": user.id, "email": email}

    @staticmethod
    def login(data):
        identifier = data.get('login_id') or data.get('email')
        password = data.get('password')

        if not identifier or not password:
            raise APIError("Login ID/Email and password are required", "VALIDATION_ERROR", 400)

        user = None
        if '@' in identifier:
            user = User.query.filter_by(email=identifier).first()
        else:
            employee = Employee.query.filter_by(employee_login_id=identifier).first()
            if employee:
                user = employee.user

        if not user:
            raise APIError("Invalid credentials", "INVALID_CREDENTIALS", 401)
        if not verify_password(password, user.password_hash):
            raise APIError("Invalid credentials", "INVALID_CREDENTIALS", 401)
        if not user.email_verified:
            raise APIError("Email not verified. Please verify your email.", "EMAIL_NOT_VERIFIED", 403)

        employee_id = None
        if user.role == 'EMPLOYEE':
            employee = Employee.query.filter_by(user_id=user.id).first()
            if employee:
                employee_id = employee.id

        access_token = create_access_token(identity={
            'user_id': user.id,
            'role': user.role,
            'employee_id': employee_id
        })

        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'must_change_password': user.must_change_password,
                'employee_id': employee_id
            }
        }

    @staticmethod
    def verify_email(token):
        verification = EmailVerificationToken.query.filter_by(token=token, used=False).first()
        if not verification:
            raise APIError("Invalid or expired token", "INVALID_TOKEN", 400)
        if verification.expires_at < datetime.utcnow():
            raise APIError("Verification token has expired", "TOKEN_EXPIRED", 400)

        user = User.query.get(verification.user_id)
        if not user:
            raise APIError("User not found", "NOT_FOUND", 404)

        user.email_verified = True
        verification.used = True
        db.session.commit()

        return {"verified": True, "user_id": user.id}

    @staticmethod
    def change_password(data):
        from flask_jwt_extended import get_jwt_identity
        identity = get_jwt_identity()
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            raise APIError("Both current and new password are required", "VALIDATION_ERROR", 400)
        if len(new_password) < 8:
            raise APIError("New password must be at least 8 characters", "WEAK_PASSWORD", 400)

        user = User.query.get(identity['user_id'])
        if not user:
            raise APIError("User not found", "NOT_FOUND", 404)
        if not verify_password(current_password, user.password_hash):
            raise APIError("Current password is incorrect", "INVALID_PASSWORD", 401)

        user.password_hash = hash_password(new_password)
        user.must_change_password = False
        db.session.commit()

        return {"changed": True}

    @staticmethod
    def forgot_password(email):
        if not email:
            raise APIError("Email is required", "VALIDATION_ERROR", 400)
        user = User.query.filter_by(email=email).first()
        if not user:
            # For security, return generic message
            return {"sent": True}
        
        # In production, create a reset token and send email
        # For now, return success without doing anything
        return {"sent": True}

    @staticmethod
    def reset_password(data):
        token = data.get('token')
        new_password = data.get('new_password')
        if not token or not new_password:
            raise APIError("Token and new password are required", "VALIDATION_ERROR", 400)
        # In production, verify token, find user, update password
        return {"reset": True}