#app/routes/auth_routes.py


from flask import Blueprint, request
from ..services.auth_service import AuthService
from ..schemas.auth_schema import RegisterSchema, LoginSchema, VerifyEmailSchema, ChangePasswordSchema, ForgotPasswordSchema, ResetPasswordSchema
from ..utils.response import success_response
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    schema = RegisterSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    result = AuthService.register_company(validated)
    return success_response(result, "Registration successful. Please check your email to verify your account.", 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    schema = LoginSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    result = AuthService.login(validated)
    return success_response(result, "Login successful")

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    data = request.get_json()
    schema = VerifyEmailSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    result = AuthService.verify_email(validated['token'])
    return success_response(result, "Email verified successfully")

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    schema = ChangePasswordSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    result = AuthService.change_password(validated)
    return success_response(result, "Password changed successfully")

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    schema = ForgotPasswordSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    result = AuthService.forgot_password(validated['email'])
    return success_response(result, "Password reset email sent")

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    schema = ResetPasswordSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    result = AuthService.reset_password(validated)
    return success_response(result, "Password reset successfully")