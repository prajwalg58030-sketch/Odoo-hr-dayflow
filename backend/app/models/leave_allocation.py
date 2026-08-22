from .. import db


class LeaveAllocation(db.Model):
    __tablename__ = 'leave_allocations'

    id = db.Column(db.Integer, primary_key=True)

    employee_id = db.Column(
        db.Integer,
        db.ForeignKey('employees.id'),
        nullable=False
    )

    leave_type_id = db.Column(
        db.Integer,
        db.ForeignKey('leave_types.id'),
        nullable=False
    )

    allocated_days = db.Column(
        db.Numeric(5, 2),
        nullable=False
    )

    used_days = db.Column(
        db.Numeric(5, 2),
        default=0
    )

    remaining_days = db.Column(
        db.Numeric(5, 2)
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            'employee_id',
            'leave_type_id',
            'year',
            name='uq_employee_leave_year'
        ),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'leave_type_id': self.leave_type_id,
            'leave_type_name': (
                self.leave_type.name
                if self.leave_type else None
            ),
            'allocated_days': (
                float(self.allocated_days)
                if self.allocated_days is not None else None
            ),
            'used_days': (
                float(self.used_days)
                if self.used_days is not None else None
            ),
            'remaining_days': (
                float(self.remaining_days)
                if self.remaining_days is not None else None
            ),
            'year': self.year
        }