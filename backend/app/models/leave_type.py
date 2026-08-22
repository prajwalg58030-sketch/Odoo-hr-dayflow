from .. import db

class LeaveType(db.Model):
    __tablename__ = 'leave_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    
    requests = db.relationship('LeaveRequest', backref='leave_type', lazy=True)
    allocations = db.relationship('LeaveAllocation', backref='leave_type', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'active': self.active
        }