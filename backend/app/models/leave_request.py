from .. import db
from datetime import datetime

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Numeric(5,2), nullable=False)
    remarks = db.Column(db.Text)
    status = db.Column(db.String(20), default='PENDING')  # PENDING, APPROVED, REJECTED, CANCELLED
    admin_comment = db.Column(db.Text)
    attachment_path = db.Column(db.String(255))
    approved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type_id': self.leave_type_id,
            'leave_type_name': self.leave_type.name if self.leave_type else None,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'days': float(self.days) if self.days is not None else None,
            'remarks': self.remarks,
            'status': self.status,
            'admin_comment': self.admin_comment,
            'attachment_path': self.attachment_path,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }