from .. import db
from datetime import datetime, date

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in = db.Column(db.DateTime)
    check_out = db.Column(db.DateTime)
    work_hours = db.Column(db.Numeric(5,2))
    extra_hours = db.Column(db.Numeric(5,2))
    status = db.Column(db.String(20), default='PRESENT')  # PRESENT, ABSENT, LATE, HALF_DAY
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='uq_employee_date'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.isoformat() if self.date else None,
            'check_in': self.check_in.isoformat() if self.check_in else None,
            'check_out': self.check_out.isoformat() if self.check_out else None,
            'work_hours': float(self.work_hours) if self.work_hours is not None else None,
            'extra_hours': float(self.extra_hours) if self.extra_hours is not None else None,
            'status': self.status
        }