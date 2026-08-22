#app/routes/attendance_routes.py

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.attendance_service import AttendanceService
from ..utils.response import success_response
from ..utils.decorators import hr_required

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/check-in', methods=['POST'])
@jwt_required()
def check_in():
    identity = get_jwt_identity()
    attendance = AttendanceService.check_in(identity['employee_id'])
    return success_response(attendance, "Check-in successful", 201)

@attendance_bp.route('/check-out', methods=['POST'])
@jwt_required()
def check_out():
    identity = get_jwt_identity()
    attendance = AttendanceService.check_out(identity['employee_id'])
    return success_response(attendance, "Check-out successful")

@attendance_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_attendance():
    identity = get_jwt_identity()
    params = request.args.to_dict()
    attendance = AttendanceService.get_employee_attendance(identity['employee_id'], params)
    return success_response(attendance)

@attendance_bp.route('/me/summary', methods=['GET'])
@jwt_required()
def get_my_summary():
    identity = get_jwt_identity()
    summary = AttendanceService.get_employee_summary(identity['employee_id'])
    return success_response(summary)

@attendance_bp.route('', methods=['GET'])
@hr_required
def get_all_attendance():
    params = request.args.to_dict()
    attendance = AttendanceService.get_all_attendance(params)
    return success_response(attendance)

@attendance_bp.route('/employee/<int:employee_id>', methods=['GET'])
@hr_required
def get_employee_attendance(employee_id):
    params = request.args.to_dict()
    attendance = AttendanceService.get_employee_attendance(employee_id, params)
    return success_response(attendance)