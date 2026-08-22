from flask_jwt_extended import create_access_token

from ..models import User, Employee
from .. import db
from ..utils.security import (
    hash_password,
    verify_password,
    generate_temp_password,
    generate_login_id,
    get_current_identity
)
from ..utils.validators import validate_email
from ..errors.exceptions import APIError


class AuthService:

    # ============================================================
    # REGISTER COMPANY / HR
    # ============================================================

    @staticmethod
    def register_company(data):
        company_name = data.get("company_name")
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        logo = data.get("logo")

        # ----------------------------
        # Validation
        # ----------------------------

        if not company_name or not name or not email or not password:
            raise APIError(
                "All fields are required",
                "VALIDATION_ERROR",
                400
            )

        if not validate_email(email):
            raise APIError(
                "Invalid email format",
                "INVALID_EMAIL",
                400
            )

        if len(password) < 8:
            raise APIError(
                "Password must be at least 8 characters",
                "WEAK_PASSWORD",
                400
            )

        # ----------------------------
        # Check existing user
        # ----------------------------

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            raise APIError(
                "Email already registered",
                "EMAIL_EXISTS",
                409
            )

        # ----------------------------
        # Create HR user
        # ----------------------------

        user = User(
            email=email,
            password_hash=hash_password(password),
            role="HR",

            # Email verification is disabled
            email_verified=True,

            must_change_password=False
        )

        db.session.add(user)
        db.session.flush()

        # ----------------------------
        # Commit
        # ----------------------------

        db.session.commit()

        return {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "company_name": company_name,
            "name": name,
            "phone": phone,
            "logo": logo
        }

    # ============================================================
    # LOGIN
    # ============================================================

    @staticmethod
    def login(data):

        identifier = data.get("login_id") or data.get("email")
        password = data.get("password")

        # ----------------------------
        # Validation
        # ----------------------------

        if not identifier or not password:
            raise APIError(
                "Login ID/Email and password are required",
                "VALIDATION_ERROR",
                400
            )

        user = None

        # ========================================================
        # LOGIN USING EMAIL
        # ========================================================

        if "@" in identifier:

            user = User.query.filter_by(
                email=identifier
            ).first()

        # ========================================================
        # LOGIN USING EMPLOYEE LOGIN ID
        # ========================================================

        else:

            employee = Employee.query.filter_by(
                employee_login_id=identifier
            ).first()

            if employee:
                user = employee.user

        # ----------------------------
        # User not found
        # ----------------------------

        if not user:
            raise APIError(
                "Invalid credentials",
                "INVALID_CREDENTIALS",
                401
            )

        # ----------------------------
        # Verify password
        # ----------------------------

        if not verify_password(
            password,
            user.password_hash
        ):
            raise APIError(
                "Invalid credentials",
                "INVALID_CREDENTIALS",
                401
            )

        # ========================================================
        # EMAIL VERIFICATION REMOVED
        # ========================================================
        #
        # We intentionally DO NOT check:
        #
        # if not user.email_verified:
        #
        # Email verification is disabled for this application.
        #
        # ========================================================

        employee_id = None

        # ----------------------------
        # Get employee ID
        # ----------------------------

        if user.role == "EMPLOYEE":

            employee = Employee.query.filter_by(
                user_id=user.id
            ).first()

            if employee:
                employee_id = employee.id

        # ========================================================
        # CREATE JWT
        # ========================================================

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role,
                "employee_id": employee_id
            }
        )

        # ========================================================
        # RESPONSE
        # ========================================================

        return {
            "access_token": access_token,

            "user": {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "must_change_password": user.must_change_password,
                "employee_id": employee_id
            }
        }

    # ============================================================
    # EMAIL VERIFICATION
    # ============================================================
    #
    # Email verification is disabled.
    #
    # This method is kept temporarily so that an existing
    # /verify-email route does not crash if the frontend still
    # calls it.
    #
    # ============================================================

    @staticmethod
    def verify_email(token):

        return {
            "verified": True,
            "message": "Email verification is disabled."
        }

    # ============================================================
    # CHANGE PASSWORD
    # ============================================================

    @staticmethod
    def change_password(data):

        identity = get_current_identity()

        current_password = data.get("current_password")
        new_password = data.get("new_password")

        # ----------------------------
        # Validation
        # ----------------------------

        if not current_password or not new_password:
            raise APIError(
                "Both current and new password are required",
                "VALIDATION_ERROR",
                400
            )

        if len(new_password) < 8:
            raise APIError(
                "New password must be at least 8 characters",
                "WEAK_PASSWORD",
                400
            )

        # ----------------------------
        # Get user
        # ----------------------------

        user = User.query.get(
            identity["user_id"]
        )

        if not user:
            raise APIError(
                "User not found",
                "NOT_FOUND",
                404
            )

        # ----------------------------
        # Verify current password
        # ----------------------------

        if not verify_password(
            current_password,
            user.password_hash
        ):
            raise APIError(
                "Current password is incorrect",
                "INVALID_PASSWORD",
                401
            )

        # ----------------------------
        # Update password
        # ----------------------------

        user.password_hash = hash_password(
            new_password
        )

        user.must_change_password = False

        db.session.commit()

        return {
            "changed": True
        }

    # ============================================================
    # FORGOT PASSWORD
    # ============================================================

    @staticmethod
    def forgot_password(email):

        if not email:
            raise APIError(
                "Email is required",
                "VALIDATION_ERROR",
                400
            )

        user = User.query.filter_by(
            email=email
        ).first()

        # ----------------------------
        # Security:
        # Always return the same response
        # ----------------------------

        if not user:
            return {
                "sent": True
            }

        # --------------------------------------------------------
        # Password reset email is not implemented yet.
        #
        # We intentionally don't expose whether the account exists.
        # --------------------------------------------------------

        return {
            "sent": True
        }

    # ============================================================
    # RESET PASSWORD
    # ============================================================

    @staticmethod
    def reset_password(data):

        token = data.get("token")
        new_password = data.get("new_password")

        # ----------------------------
        # Validation
        # ----------------------------

        if not token or not new_password:
            raise APIError(
                "Token and new password are required",
                "VALIDATION_ERROR",
                400
            )

        if len(new_password) < 8:
            raise APIError(
                "New password must be at least 8 characters",
                "WEAK_PASSWORD",
                400
            )

        # --------------------------------------------------------
        # Password reset token system is not implemented yet.
        # --------------------------------------------------------

        return {
            "reset": True
        }