#app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from .config.database import DatabaseConfig
from .config.security import SecurityConfig
from .config.mail import MailConfig
from .errors.handlers import register_error_handlers
from .routes import register_routes

db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(DatabaseConfig)
    app.config.from_object(SecurityConfig)
    app.config.from_object(MailConfig)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    mail.init_app(app)
    
    # Register routes and error handlers
    register_routes(app)
    register_error_handlers(app)
    
    # Create tables if not exist (development only)
    with app.app_context():
        db.create_all()
    
    return app