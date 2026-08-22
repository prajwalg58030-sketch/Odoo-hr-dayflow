from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    company_name = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    logo = fields.Str(required=False)  # Base64 or path

class LoginSchema(Schema):
    login_id = fields.Str(required=False)
    email = fields.Email(required=False)
    password = fields.Str(required=True)

class VerifyEmailSchema(Schema):
    token = fields.Str(required=True)

class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=8))

class ForgotPasswordSchema(Schema):
    email = fields.Email(required=True)

class ResetPasswordSchema(Schema):
    token = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=8))