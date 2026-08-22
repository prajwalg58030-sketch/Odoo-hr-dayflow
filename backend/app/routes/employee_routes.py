#app/routes/employee_routes.py

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.employee_service import EmployeeService
from ..schemas.employee_schema import EmployeeCreateSchema, EmployeeUpdateSchema, EmployeeProfileUpdateSchema
from ..utils.response import success_response
from ..utils.decorators import hr_required
from marshmallow import ValidationError

employee_bp = Blueprint('employees', __name__)

@employee_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    identity = get_jwt_identity()
    employee = EmployeeService.get_employee_by_user_id(identity['user_id'])
    return success_response(employee)

@employee_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_me():
    identity = get_jwt_identity()
    data = request.get_json()
    schema = EmployeeProfileUpdateSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    employee = EmployeeService.update_employee_profile(identity['user_id'], validated)
    return success_response(employee, "Profile updated successfully")

@employee_bp.route('', methods=['GET'])
@hr_required
def get_employees():
    filters = request.args.to_dict()
    employees = EmployeeService.get_all_employees(filters)
    return success_response(employees)

@employee_bp.route('', methods=['POST'])
@hr_required
def create_employee():
    data = request.get_json()
    schema = EmployeeCreateSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    result = EmployeeService.create_employee(validated)
    return success_response(result, "Employee created successfully", 201)

@employee_bp.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    identity = get_jwt_identity()
    employee = EmployeeService.get_employee(employee_id, identity)
    return success_response(employee)

@employee_bp.route('/<int:employee_id>', methods=['PUT'])
@hr_required
def update_employee(employee_id):
    data = request.get_json()
    schema = EmployeeUpdateSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    employee = EmployeeService.update_employee(employee_id, validated)
    return success_response(employee, "Employee updated successfully")