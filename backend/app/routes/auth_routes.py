from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from marshmallow import ValidationError

from ..schemas.auth_schema import (
    RegisterSchema,
    LoginSchema,
    ChangePasswordSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema
)

from ..services.auth_service import AuthService

from ..utils.response import success_response


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# ============================================================
# REGISTER COMPANY / HR
# ============================================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json() or {}

    schema = RegisterSchema()

    try:
        validated = schema.load(data)

    except ValidationError as e:

        return success_response(
            None,
            str(e.messages),
            400
        )

    result = AuthService.register_company(
        validated
    )

    return success_response(
        result,
        "Registration successful",
        201
    )


# ============================================================
# LOGIN
# ============================================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json() or {}

    schema = LoginSchema()

    try:
        validated = schema.load(data)

    except ValidationError as e:

        return success_response(
            None,
            str(e.messages),
            400
        )

    result = AuthService.login(
        validated
    )

    return success_response(
        result,
        "Login successful"
    )


@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():

    data = request.get_json() or {}
    token = data.get("token")

    if not token:
        return success_response(None, "Verification token is required", 400)

    result = AuthService.verify_email(token)

    return success_response(
        result,
        "Email verification successful"
    )


# ============================================================
# CHANGE PASSWORD
# ============================================================

@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():

    data = request.get_json() or {}

    schema = ChangePasswordSchema()

    try:
        validated = schema.load(data)

    except ValidationError as e:

        return success_response(
            None,
            str(e.messages),
            400
        )

    result = AuthService.change_password(
        validated
    )

    return success_response(
        result,
        "Password changed successfully"
    )


# ============================================================
# FORGOT PASSWORD
# ============================================================

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json() or {}

    schema = ForgotPasswordSchema()

    try:
        validated = schema.load(data)

    except ValidationError as e:

        return success_response(
            None,
            str(e.messages),
            400
        )

    result = AuthService.forgot_password(
        validated["email"]
    )

    return success_response(
        result,
        "If the account exists, password reset instructions will be sent"
    )


# ============================================================
# RESET PASSWORD
# ============================================================

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json() or {}

    schema = ResetPasswordSchema()

    try:
        validated = schema.load(data)

    except ValidationError as e:

        return success_response(
            None,
            str(e.messages),
            400
        )

    result = AuthService.reset_password(
        validated
    )

    return success_response(
        result,
        "Password reset successfully"
    )