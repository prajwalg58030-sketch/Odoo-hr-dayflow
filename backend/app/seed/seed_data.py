from .. import db
from ..models import User, Employee, LeaveType, LeaveAllocation, Salary
from ..utils.security import hash_password, generate_login_id
from datetime import date
import os

def seed_data():
    # Only run if no data exists
    if User.query.count() > 0:
        print("Database already seeded. Skipping.")
        return

    print("Seeding database...")

    # Create HR admin
    hr_user = User(
        email=os.getenv('HR_EMAIL', 'hr@dayflow.com'),
        password_hash=hash_password(os.getenv('HR_PASSWORD', 'Admin@123')),
        role='HR',
        email_verified=True,
        must_change_password=False
    )
    db.session.add(hr_user)
    db.session.flush()

    # Create leave types
    pto = LeaveType(name='Paid Time Off', description='Paid leave for vacation', active=True)
    sick = LeaveType(name='Sick Leave', description='Sick leave with certificate', active=True)
    unpaid = LeaveType(name='Unpaid Leave', description='Unpaid leave', active=True)
    db.session.add_all([pto, sick, unpaid])
    db.session.flush()

    # Create demo employee
    emp_user = User(
        email=os.getenv('DEMO_EMPLOYEE_EMAIL', 'john.doe@dayflow.com'),
        password_hash=hash_password(os.getenv('DEMO_EMPLOYEE_PASSWORD', 'Employee@123')),
        role='EMPLOYEE',
        email_verified=True,
        must_change_password=True
    )
    db.session.add(emp_user)
    db.session.flush()

    emp = Employee(
        user_id=emp_user.id,
        employee_login_id='OIJODO20260001',
        first_name='John',
        last_name='Doe',
        phone='+1 555-1234',
        address='123 Main St, City',
        department='Engineering',
        designation='Software Engineer',
        joining_date=date(2026, 1, 15)
    )
    db.session.add(emp)
    db.session.flush()

    # Leave allocations for demo employee (current year)
    year = date.today().year
    db.session.add(LeaveAllocation(
        employee_id=emp.id,
        leave_type_id=pto.id,
        allocated_days=24,
        used_days=0,
        remaining_days=24,
        year=year
    ))
    db.session.add(LeaveAllocation(
        employee_id=emp.id,
        leave_type_id=sick.id,
        allocated_days=7,
        used_days=0,
        remaining_days=7,
        year=year
    ))
    db.session.add(LeaveAllocation(
        employee_id=emp.id,
        leave_type_id=unpaid.id,
        allocated_days=0,
        used_days=0,
        remaining_days=0,
        year=year
    ))

    # Salary for demo employee
    components = {
        'monthly_wage': 50000,
        'basic_salary': 25000,
        'hra': 12500,
        'standard_allowance': 5000,
        'performance_bonus': 2082.5,
        'lta': 2082.5,
        'fixed_allowance': 3335,
        'pf': 3000,
        'professional_tax': 200,
        'other_deductions': 0,
        'gross_salary': 50000,
        'net_salary': 46800
    }
    db.session.add(Salary(
        employee_id=emp.id,
        **components,
        effective_from=date.today()
    ))

    db.session.commit()
    print("Database seeded successfully.")