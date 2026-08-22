from marshmallow import Schema, fields, validate

class LeaveApplySchema(Schema):
    leave_type_id = fields.Int(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    remarks = fields.Str(required=False)
    attachment_path = fields.Str(required=False)  # optional, file path after upload

class LeaveRejectSchema(Schema):
    admin_comment = fields.Str(required=False)