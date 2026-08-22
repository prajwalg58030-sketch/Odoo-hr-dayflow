from datetime import datetime
from ..models import User, Employee
from .. import db
from ..utils.security import hash_password, generate_temp_password, generate_login_id
from ..utils.validators import validate_email, validate_phone
from ..errors.exceptions import APIError
from .email_service import EmailService

class EmployeeService:

    @staticmethod
    def create_employee(data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        department = data.get('department')
        designation = data.get('designation')
        joining_date_str = data.get('joining_date')
        address = data.get('address')
        profile_picture = data.get('profile_picture')

        if not first_name or not last_name or not email or not joining_date_str:
            raise APIError("First name, last name, email, and joining date are required", "VALIDATION_ERROR", 400)
        if len(first_name) < 2 or len(last_name) < 2:
            raise APIError("First name and last name must be at least 2 characters", "VALIDATION_ERROR", 400)
        if not validate_email(email):
            raise APIError("Invalid email format", "INVALID_EMAIL", 400)
        if not phone or not validate_phone(phone):
            raise APIError("Invalid phone number", "INVALID_PHONE", 400)

        if User.query.filter_by(email=email).first():
            raise APIError("Email already exists", "EMAIL_EXISTS", 409)

        joining_date = datetime.strptime(joining_date_str, '%Y-%m-%d').date()
        year = joining_date.year
        employees_this_year = Employee.query.filter(
            Employee.employee_login_id.like(f'%{year}%')
        ).count()
        serial = employees_this_year + 1

        login_id = generate_login_id(first_name, last_name, year, serial)
        while Employee.query.filter_by(employee_login_id=login_id).first():
            serial += 1
            login_id = generate_login_id(first_name, last_name, year, serial)

        temp_password = generate_temp_password()
        password_hash = hash_password(temp_password)

        user = User(
            email=email,
            password_hash=password_hash,
            role='EMPLOYEE',
            email_verified=True,  # Employees are pre-verified by HR
            must_change_password=True
        )
        db.session.add(user)
        db.session.flush()

        employee = Employee(
            user_id=user.id,
            employee_login_id=login_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            department=department,
            designation=designation,
            joining_date=joining_date,
            profile_picture=profile_picture
        )
        db.session.add(employee)
        db.session.commit()

        EmailService.send_employee_credentials(email, login_id, temp_password)

        return {
            'employee_id': employee.id,
            'login_id': login_id,
            'temp_password': temp_password
        }

    @staticmethod
    def get_all_employees(filters=None):
        query = Employee.query
        if filters:
            search = filters.get('search')
            department = filters.get('department')
            if search:
                query = query.filter(
                    (Employee.first_name.ilike(f'%{search}%')) |
                    (Employee.last_name.ilike(f'%{search}%')) |
                    (Employee.employee_login_id.ilike(f'%{search}%'))
                )
            if department:
                query = query.filter(Employee.department == department)
        employees = query.all()
        return [emp.to_dict() for emp in employees]

    @staticmethod
    def get_employee_by_user_id(user_id):
        employee = Employee.query.filter_by(user_id=user_id).first()
        if not employee:
            raise APIError("Employee profile not found", "NOT_FOUND", 404)
        return employee.to_dict()

    @staticmethod
    def get_employee(employee_id, identity):
        employee = Employee.query.get(employee_id)
        if not employee:
            raise APIError("Employee not found", "NOT_FOUND", 404)
        if identity['role'] != 'HR' and identity.get('employee_id') != employee_id:
            raise APIError("Access denied", "FORBIDDEN", 403)
        return employee.to_dict()

    @staticmethod
    def update_employee_profile(user_id, data):
        employee = Employee.query.filter_by(user_id=user_id).first()
        if not employee:
            raise APIError("Employee not found", "NOT_FOUND", 404)
        allowed_fields = ['phone', 'address', 'profile_picture']
        for field in allowed_fields:
            if field in data:
                setattr(employee, field, data[field])
        db.session.commit()
        return employee.to_dict()

    @staticmethod
    def update_employee(employee_id, data):
        employee = Employee.query.get(employee_id)
        if not employee:
            raise APIError("Employee not found", "NOT_FOUND", 404)
        allowed_fields = ['first_name', 'last_name', 'phone', 'address', 
                          'department', 'designation', 'joining_date', 'profile_picture']
        for field in allowed_fields:
            if field in data:
                setattr(employee, field, data[field])
        db.session.commit()
        return employee.to_dict()