from flask import current_app
from flask_mail import Message
from app.config.mail import mail

class EmailService:

    @staticmethod
    def send_verification_email(email, token):
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5500')
        verification_link = f"{frontend_url}/verify-email.html?token={token}"
        msg = Message(
            "Verify your DAYFLOW HRMS account",
            recipients=[email]
        )
        msg.body = f"Please click the link to verify your email: {verification_link}"
        msg.html = f"<p>Click <a href='{verification_link}'>here</a> to verify your email.</p>"
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Failed to send verification email: {e}")

    @staticmethod
    def send_employee_credentials(email, login_id, temp_password):
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5500')
        login_link = f"{frontend_url}/login.html"
        msg = Message(
            "Your DAYFLOW HRMS account credentials",
            recipients=[email]
        )
        msg.body = f"Welcome to DAYFLOW HRMS!\n\nYour Login ID: {login_id}\nTemporary Password: {temp_password}\nLogin at: {login_link}"
        msg.html = f"""
        <p>Welcome to DAYFLOW HRMS!</p>
        <p>Your Login ID: <strong>{login_id}</strong></p>
        <p>Temporary Password: <strong>{temp_password}</strong></p>
        <p>Login at: <a href='{login_link}'>{login_link}</a></p>
        <p>You will be required to change your password after first login.</p>
        """
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Failed to send employee credentials email: {e}")