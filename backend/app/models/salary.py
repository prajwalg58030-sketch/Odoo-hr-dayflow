from .. import db
from datetime import datetime, date

class Salary(db.Model):
    __tablename__ = 'salaries'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    monthly_wage = db.Column(db.Numeric(12,2), nullable=False)
    basic_salary = db.Column(db.Numeric(12,2))
    hra = db.Column(db.Numeric(12,2))
    standard_allowance = db.Column(db.Numeric(12,2))
    performance_bonus = db.Column(db.Numeric(12,2))
    lta = db.Column(db.Numeric(12,2))
    fixed_allowance = db.Column(db.Numeric(12,2))
    pf = db.Column(db.Numeric(12,2))
    professional_tax = db.Column(db.Numeric(12,2))
    other_deductions = db.Column(db.Numeric(12,2))
    gross_salary = db.Column(db.Numeric(12,2))
    net_salary = db.Column(db.Numeric(12,2))
    effective_from = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'monthly_wage': float(self.monthly_wage) if self.monthly_wage is not None else None,
            'basic_salary': float(self.basic_salary) if self.basic_salary is not None else None,
            'hra': float(self.hra) if self.hra is not None else None,
            'standard_allowance': float(self.standard_allowance) if self.standard_allowance is not None else None,
            'performance_bonus': float(self.performance_bonus) if self.performance_bonus is not None else None,
            'lta': float(self.lta) if self.lta is not None else None,
            'fixed_allowance': float(self.fixed_allowance) if self.fixed_allowance is not None else None,
            'pf': float(self.pf) if self.pf is not None else None,
            'professional_tax': float(self.professional_tax) if self.professional_tax is not None else None,
            'other_deductions': float(self.other_deductions) if self.other_deductions is not None else None,
            'gross_salary': float(self.gross_salary) if self.gross_salary is not None else None,
            'net_salary': float(self.net_salary) if self.net_salary is not None else None,
            'effective_from': self.effective_from.isoformat() if self.effective_from else None
        }