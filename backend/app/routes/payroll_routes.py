#app/routes/payroll_routes.py

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.payroll_service import PayrollService
from ..schemas.payroll_schema import SalaryUpdateSchema
from ..utils.response import success_response
from ..utils.decorators import hr_required
from marshmallow import ValidationError

payroll_bp = Blueprint('payroll', __name__)

@payroll_bp.route('/payroll/me', methods=['GET'])
@jwt_required()
def get_my_payroll():
    identity = get_jwt_identity()
    payroll = PayrollService.get_employee_payroll(identity['employee_id'])
    return success_response(payroll)

@payroll_bp.route('/payroll', methods=['GET'])
@hr_required
def get_all_payroll():
    params = request.args.to_dict()
    payroll = PayrollService.get_all_payroll(params)
    return success_response(payroll)

@payroll_bp.route('/payroll/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee_payroll(employee_id):
    identity = get_jwt_identity()
    payroll = PayrollService.get_employee_payroll(employee_id, identity)
    return success_response(payroll)

@payroll_bp.route('/payroll/<int:employee_id>', methods=['PUT'])
@hr_required
def update_employee_payroll(employee_id):
    data = request.get_json()
    schema = SalaryUpdateSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    payroll = PayrollService.update_employee_payroll(employee_id, validated)
    return success_response(payroll, "Payroll updated successfully")

@payroll_bp.route('/salary-structure/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_salary_structure(employee_id):
    identity = get_jwt_identity()
    structure = PayrollService.get_salary_structure(employee_id, identity)
    return success_response(structure)

@payroll_bp.route('/salary-structure/<int:employee_id>', methods=['PUT'])
@hr_required
def update_salary_structure(employee_id):
    data = request.get_json()
    schema = SalaryUpdateSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    structure = PayrollService.update_salary_structure(employee_id, validated)
    return success_response(structure, "Salary structure updated")