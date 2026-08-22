from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask import jsonify
from .security import get_current_identity

def hr_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_current_identity()
        if identity.get('role') != 'HR':
            return jsonify({
                "success": False,
                "message": "HR access required",
                "error": "FORBIDDEN"
            }), 403
        return fn(*args, **kwargs)
    return wrapper

def employee_or_hr_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        identity = get_current_identity()
        if identity.get('role') not in ['HR', 'EMPLOYEE']:
            return jsonify({
                "success": False,
                "message": "Authentication required",
                "error": "UNAUTHORIZED"
            }), 401
        return fn(*args, **kwargs)
    return wrapper