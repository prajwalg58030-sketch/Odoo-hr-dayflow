from datetime import datetime, date
from ..models import LeaveRequest, LeaveType, Employee
from app.config.database import db
from ..errors.exceptions import APIError

class LeaveService:

    @staticmethod
    def apply_leave(employee_id, data):
        leave_type_id = data.get('leave_type_id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')
        remarks = data.get('remarks', '')
        attachment_path = data.get('attachment_path')

        if not leave_type_id or not start_date_str or not end_date_str:
            raise APIError("Leave type, start date and end date are required", "VALIDATION_ERROR", 400)

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        if start_date > end_date:
            raise APIError("Start date cannot be after end date", "INVALID_DATES", 400)

        days = (end_date - start_date).days + 1
        leave_type = LeaveType.query.get(leave_type_id)
        if not leave_type or not leave_type.active:
            raise APIError("Invalid leave type", "INVALID_LEAVE_TYPE", 400)

        # Check allocation
        allocation = LeaveAllocation.query.filter_by(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            year=start_date.year
        ).first()
        if not allocation:
            # Auto-allocate default
            if leave_type.name == 'Paid Time Off':
                allocated = 24
            elif leave_type.name == 'Sick Leave':
                allocated = 7
            elif leave_type.name == 'Unpaid Leave':
                allocated = 0  # unlimited or no allocation
            else:
                allocated = 0
            allocation = LeaveAllocation(
                employee_id=employee_id,
                leave_type_id=leave_type_id,
                year=start_date.year,
                allocated_days=allocated,
                used_days=0,
                remaining_days=allocated
            )
            db.session.add(allocation)
            db.session.flush()

        if allocation.remaining_days < days:
            raise APIError("Insufficient leave balance", "INSUFFICIENT_LEAVE_BALANCE", 400)

        leave_request = LeaveRequest(
            employee_id=employee_id,
            leave_type_id=leave_type_id,
            start_date=start_date,
            end_date=end_date,
            days=days,
            remarks=remarks,
            status='PENDING',
            attachment_path=attachment_path
        )
        db.session.add(leave_request)
        db.session.commit()
        return leave_request.to_dict()

    @staticmethod
    def get_employee_leaves(employee_id):
        leaves = LeaveRequest.query.filter_by(employee_id=employee_id).order_by(LeaveRequest.start_date.desc()).all()
        return [leave.to_dict() for leave in leaves]

    @staticmethod
    def get_all_leaves(params=None):
        query = LeaveRequest.query.order_by(LeaveRequest.start_date.desc())
        if params:
            if 'employee_id' in params:
                query = query.filter(LeaveRequest.employee_id == params['employee_id'])
            if 'status' in params:
                query = query.filter(LeaveRequest.status == params['status'])
            if 'leave_type_id' in params:
                query = query.filter(LeaveRequest.leave_type_id == params['leave_type_id'])
        leaves = query.all()
        return [leave.to_dict() for leave in leaves]

    @staticmethod
    def get_leave(leave_id, identity):
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            raise APIError("Leave request not found", "NOT_FOUND", 404)
        if identity['role'] != 'HR' and identity.get('employee_id') != leave.employee_id:
            raise APIError("Access denied", "FORBIDDEN", 403)
        return leave.to_dict()

    @staticmethod
    def approve_leave(leave_id, hr_user_id):
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            raise APIError("Leave request not found", "NOT_FOUND", 404)
        if leave.status != 'PENDING':
            raise APIError("Leave request already processed", "ALREADY_PROCESSED", 409)

        leave.status = 'APPROVED'
        leave.approved_at = datetime.utcnow()
        allocation = LeaveAllocation.query.filter_by(
            employee_id=leave.employee_id,
            leave_type_id=leave.leave_type_id,
            year=leave.start_date.year
        ).first()
        if allocation:
            allocation.used_days = float(allocation.used_days) + float(leave.days)
            allocation.remaining_days = float(allocation.allocated_days) - float(allocation.used_days)
        db.session.commit()
        return leave.to_dict()

    @staticmethod
    def reject_leave(leave_id, hr_user_id, admin_comment=''):
        leave = LeaveRequest.query.get(leave_id)
        if not leave:
            raise APIError("Leave request not found", "NOT_FOUND", 404)
        if leave.status != 'PENDING':
            raise APIError("Leave request already processed", "ALREADY_PROCESSED", 409)

        leave.status = 'REJECTED'
        leave.admin_comment = admin_comment
        db.session.commit()
        return leave.to_dict()

    @staticmethod
    def get_employee_allocations(employee_id):
        allocations = LeaveAllocation.query.filter_by(employee_id=employee_id).all()
        return [alloc.to_dict() for alloc in allocations]

    @staticmethod
    def get_all_allocations():
        allocations = LeaveAllocation.query.all()
        return [alloc.to_dict() for alloc in allocations]