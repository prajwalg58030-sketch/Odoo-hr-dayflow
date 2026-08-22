from datetime import datetime, date, timedelta
from ..models import Attendance, Employee
from .. import db
from ..errors.exceptions import APIError

class AttendanceService:

    @staticmethod
    def check_in(employee_id):
        today = date.today()
        existing = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if existing:
            if existing.check_in:
                raise APIError("You have already checked in today", "ATTENDANCE_ALREADY_EXISTS", 409)
        now = datetime.utcnow()
        if not existing:
            attendance = Attendance(employee_id=employee_id, date=today, check_in=now, status='PRESENT')
            db.session.add(attendance)
        else:
            existing.check_in = now
            existing.status = 'PRESENT'
            attendance = existing
        db.session.commit()
        return {
            'attendance_id': attendance.id,
            'check_in': attendance.check_in.strftime('%Y-%m-%d %H:%M:%S'),
            'status': attendance.status
        }

    @staticmethod
    def check_out(employee_id):
        today = date.today()
        attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
        if not attendance or not attendance.check_in:
            raise APIError("You must check in before checking out", "NO_CHECK_IN", 400)
        if attendance.check_out:
            raise APIError("You have already checked out today", "ALREADY_CHECKED_OUT", 409)

        now = datetime.utcnow()
        attendance.check_out = now
        duration = now - attendance.check_in
        work_seconds = duration.total_seconds()
        work_hours = round(work_seconds / 3600, 2)
        attendance.work_hours = work_hours

        standard_hours = 8
        extra = max(0, work_hours - standard_hours)
        attendance.extra_hours = round(extra, 2)
        attendance.status = 'CHECKED_OUT'
        db.session.commit()
        return {
            'check_out': attendance.check_out.strftime('%Y-%m-%d %H:%M:%S'),
            'work_hours': float(attendance.work_hours),
            'extra_hours': float(attendance.extra_hours),
            'status': attendance.status
        }

    @staticmethod
    def get_employee_attendance(employee_id, params=None):
        query = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.date.desc())
        if params:
            if 'from' in params:
                from_date = datetime.strptime(params['from'], '%Y-%m-%d').date()
                query = query.filter(Attendance.date >= from_date)
            if 'to' in params:
                to_date = datetime.strptime(params['to'], '%Y-%m-%d').date()
                query = query.filter(Attendance.date <= to_date)
        records = query.all()
        return [att.to_dict() for att in records]

    @staticmethod
    def get_employee_summary(employee_id):
        today = date.today()
        current_month = today.month
        current_year = today.year
        records = Attendance.query.filter_by(employee_id=employee_id).filter(
            Attendance.date >= date(current_year, current_month, 1)
        ).all()
        present = sum(1 for r in records if r.status in ['PRESENT', 'CHECKED_OUT'])
        absent = sum(1 for r in records if r.status == 'ABSENT')
        total_work_hours = sum(float(r.work_hours or 0) for r in records)
        extra_hours = sum(float(r.extra_hours or 0) for r in records)
        return {
            'month': f"{today.strftime('%B')} {current_year}",
            'present_days': present,
            'absent_days': absent,
            'total_work_hours': round(total_work_hours, 2),
            'extra_hours': round(extra_hours, 2)
        }

    @staticmethod
    def get_all_attendance(params=None):
        query = Attendance.query.order_by(Attendance.date.desc())
        if params:
            if 'employee_id' in params:
                query = query.filter(Attendance.employee_id == params['employee_id'])
            if 'from' in params:
                from_date = datetime.strptime(params['from'], '%Y-%m-%d').date()
                query = query.filter(Attendance.date >= from_date)
            if 'to' in params:
                to_date = datetime.strptime(params['to'], '%Y-%m-%d').date()
                query = query.filter(Attendance.date <= to_date)
        records = query.all()
        return [att.to_dict() for att in records]