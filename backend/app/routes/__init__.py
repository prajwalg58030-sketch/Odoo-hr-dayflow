#app/routes/__init__.py

from .auth_routes import auth_bp
from .employee_routes import employee_bp
from .attendance_routes import attendance_bp
from .leave_routes import leave_bp
from .payroll_routes import payroll_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(employee_bp, url_prefix='/api/employees')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(leave_bp, url_prefix='/api')
    app.register_blueprint(payroll_bp, url_prefix='/api')