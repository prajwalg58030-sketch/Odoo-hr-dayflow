from datetime import date
from decimal import Decimal
from ..models import Salary, Employee, Attendance
from app.config.database import db
from ..errors.exceptions import APIError

class PayrollService:

    @staticmethod
    def _calculate_salary_components(monthly_wage):
        # Configuration (could be from config)
        basic_pct = Decimal('0.50')
        hra_pct = Decimal('0.50')  # of basic
        perf_bonus_pct = Decimal('0.0833')
        lta_pct = Decimal('0.0833')
        pf_pct = Decimal('0.12')
        prof_tax = Decimal('200')
        standard_allowance_pct = Decimal('0.10')
        fixed_allowance = Decimal('0.00')

        monthly_wage = Decimal(str(monthly_wage))
        basic_salary = monthly_wage * basic_pct
        hra = basic_salary * hra_pct
        standard_allowance = monthly_wage * standard_allowance_pct
        performance_bonus = basic_salary * perf_bonus_pct
        lta = basic_salary * lta_pct

        total_earnings = basic_salary + hra + standard_allowance + performance_bonus + lta
        fixed_allowance = monthly_wage - total_earnings
        if fixed_allowance < 0:
            fixed_allowance = Decimal('0.00')

        gross_salary = basic_salary + hra + standard_allowance + performance_bonus + lta + fixed_allowance

        pf = basic_salary * pf_pct
        professional_tax = prof_tax
        other_deductions = Decimal('0.00')
        total_deductions = pf + professional_tax + other_deductions

        net_salary = gross_salary - total_deductions

        return {
            'monthly_wage': monthly_wage,
            'basic_salary': basic_salary,
            'hra': hra,
            'standard_allowance': standard_allowance,
            'performance_bonus': performance_bonus,
            'lta': lta,
            'fixed_allowance': fixed_allowance,
            'pf': pf,
            'professional_tax': professional_tax,
            'other_deductions': other_deductions,
            'gross_salary': gross_salary,
            'net_salary': net_salary
        }

    @staticmethod
    def get_employee_payroll(employee_id, identity=None):
        if identity and identity.get('role') != 'HR' and identity.get('employee_id') != employee_id:
            raise APIError("Access denied", "FORBIDDEN", 403)
        salary = Salary.query.filter_by(employee_id=employee_id).order_by(Salary.effective_from.desc()).first()
        if not salary:
            raise APIError("Salary structure not found", "NOT_FOUND", 404)
        return salary.to_dict()

    @staticmethod
    def get_all_payroll(params=None):
        query = Salary.query.order_by(Salary.effective_from.desc())
        salaries = query.all()
        return [s.to_dict() for s in salaries]

    @staticmethod
    def update_employee_payroll(employee_id, data):
        monthly_wage = data.get('monthly_wage')
        if not monthly_wage:
            raise APIError("Monthly wage is required", "VALIDATION_ERROR", 400)
        components = PayrollService._calculate_salary_components(monthly_wage)
        salary = Salary(
            employee_id=employee_id,
            **components,
            effective_from=date.today()
        )
        db.session.add(salary)
        db.session.commit()
        return salary.to_dict()

    @staticmethod
    def get_salary_structure(employee_id, identity=None):
        if identity and identity.get('role') != 'HR' and identity.get('employee_id') != employee_id:
            raise APIError("Access denied", "FORBIDDEN", 403)
        salary = Salary.query.filter_by(employee_id=employee_id).order_by(Salary.effective_from.desc()).first()
        if not salary:
            raise APIError("Salary structure not found", "NOT_FOUND", 404)
        return salary.to_dict()

    @staticmethod
    def update_salary_structure(employee_id, data):
        # Support direct update or recalculate
        if 'monthly_wage' in data:
            components = PayrollService._calculate_salary_components(data['monthly_wage'])
            data.update(components)
        # Remove None values to avoid overwriting with None
        cleaned_data = {k: v for k, v in data.items() if v is not None}
        salary = Salary(
            employee_id=employee_id,
            **cleaned_data,
            effective_from=date.today()
        )
        db.session.add(salary)
        db.session.commit()
        return salary.to_dict()