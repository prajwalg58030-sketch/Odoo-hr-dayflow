from marshmallow import Schema, fields, validate

class EmployeeCreateSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=2))
    last_name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    department = fields.Str(required=False)
    designation = fields.Str(required=False)
    joining_date = fields.Date(required=True)
    address = fields.Str(required=False)
    profile_picture = fields.Str(required=False)  # base64 or path

class EmployeeUpdateSchema(Schema):
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    phone = fields.Str(required=False)
    address = fields.Str(required=False)
    department = fields.Str(required=False)
    designation = fields.Str(required=False)
    joining_date = fields.Date(required=False)
    profile_picture = fields.Str(required=False)

class EmployeeProfileUpdateSchema(Schema):
    phone = fields.Str(required=False)
    address = fields.Str(required=False)
    profile_picture = fields.Str(required=False)