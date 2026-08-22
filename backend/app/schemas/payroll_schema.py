from marshmallow import Schema, fields, validate

class SalaryUpdateSchema(Schema):
    monthly_wage = fields.Decimal(required=True, places=2)
    # Other components optional; if not provided, recalculated
    basic_salary = fields.Decimal(required=False)
    hra = fields.Decimal(required=False)
    standard_allowance = fields.Decimal(required=False)
    performance_bonus = fields.Decimal(required=False)
    lta = fields.Decimal(required=False)
    fixed_allowance = fields.Decimal(required=False)
    pf = fields.Decimal(required=False)
    professional_tax = fields.Decimal(required=False)
    other_deductions = fields.Decimal(required=False)