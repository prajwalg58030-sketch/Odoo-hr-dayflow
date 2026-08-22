from marshmallow import Schema, fields

class AttendanceSchema(Schema):
    id = fields.Int(dump_only=True)
    employee_id = fields.Int()
    date = fields.Date()
    check_in = fields.DateTime()
    check_out = fields.DateTime()
    work_hours = fields.Float()
    extra_hours = fields.Float()
    status = fields.Str()