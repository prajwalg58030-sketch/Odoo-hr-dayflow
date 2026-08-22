from marshmallow import Schema, fields, validate


# ============================================================
# REGISTER COMPANY / HR
# ============================================================

class RegisterSchema(Schema):

    company_name = fields.Str(
        required=True
    )

    name = fields.Str(
        required=True
    )

    email = fields.Email(
        required=True
    )

    phone = fields.Str(
        required=True
    )

    password = fields.Str(
        required=True,
        validate=validate.Length(min=8)
    )

    logo = fields.Str(
        required=False,
        allow_none=True
    )


# ============================================================
# LOGIN
# ============================================================

class LoginSchema(Schema):

    # Employee login ID, e.g. EMP001
    login_id = fields.Str(
        required=False,
        allow_none=True
    )

    # Email login, e.g. admin345@gmail.com
    email = fields.Email(
        required=False,
        allow_none=True
    )

    password = fields.Str(
        required=True
    )


# ============================================================
# CHANGE PASSWORD
# ============================================================

class ChangePasswordSchema(Schema):

    current_password = fields.Str(
        required=True
    )

    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8)
    )


# ============================================================
# FORGOT PASSWORD
# ============================================================

class ForgotPasswordSchema(Schema):

    email = fields.Email(
        required=True
    )


# ============================================================
# RESET PASSWORD
# ============================================================

class ResetPasswordSchema(Schema):

    token = fields.Str(
        required=True
    )

    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8)
    )