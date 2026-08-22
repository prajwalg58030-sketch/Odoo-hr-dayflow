#app/routes/leave_routes.py


from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.leave_service import LeaveService
from ..schemas.leave_schema import LeaveApplySchema, LeaveRejectSchema
from ..utils.response import success_response
from ..utils.decorators import hr_required
from marshmallow import ValidationError

leave_bp = Blueprint('leaves', __name__)

@leave_bp.route('/leaves', methods=['POST'])
@jwt_required()
def apply_leave():
    identity = get_jwt_identity()
    data = request.get_json()
    schema = LeaveApplySchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    leave = LeaveService.apply_leave(identity['employee_id'], validated)
    return success_response(leave, "Leave application submitted", 201)

@leave_bp.route('/leaves/me', methods=['GET'])
@jwt_required()
def get_my_leaves():
    identity = get_jwt_identity()
    leaves = LeaveService.get_employee_leaves(identity['employee_id'])
    return success_response(leaves)

@leave_bp.route('/leaves', methods=['GET'])
@hr_required
def get_all_leaves():
    params = request.args.to_dict()
    leaves = LeaveService.get_all_leaves(params)
    return success_response(leaves)

@leave_bp.route('/leaves/<int:leave_id>', methods=['GET'])
@jwt_required()
def get_leave(leave_id):
    identity = get_jwt_identity()
    leave = LeaveService.get_leave(leave_id, identity)
    return success_response(leave)

@leave_bp.route('/leaves/<int:leave_id>/approve', methods=['PUT'])
@hr_required
def approve_leave(leave_id):
    identity = get_jwt_identity()
    leave = LeaveService.approve_leave(leave_id, identity['user_id'])
    return success_response(leave, "Leave approved")

@leave_bp.route('/leaves/<int:leave_id>/reject', methods=['PUT'])
@hr_required
def reject_leave(leave_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    schema = LeaveRejectSchema()
    try:
        validated = schema.load(data)
    except ValidationError as e:
        return success_response(None, str(e.messages), 400)
    leave = LeaveService.reject_leave(leave_id, identity['user_id'], validated.get('admin_comment', ''))
    return success_response(leave, "Leave rejected")

@leave_bp.route('/leave-allocations/me', methods=['GET'])
@jwt_required()
def get_my_allocations():
    identity = get_jwt_identity()
    allocations = LeaveService.get_employee_allocations(identity['employee_id'])
    return success_response(allocations)

@leave_bp.route('/leave-allocations', methods=['GET'])
@hr_required
def get_all_allocations():
    allocations = LeaveService.get_all_allocations()
    return success_response(allocations)