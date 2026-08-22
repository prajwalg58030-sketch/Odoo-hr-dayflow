from flask import jsonify
from .exceptions import APIError
from ..utils.response import error_response

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(e):
        return error_response(e.message, e.error_code, e.status_code)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Resource not found", "NOT_FOUND", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error_response("Method not allowed", "METHOD_NOT_ALLOWED", 405)

    @app.errorhandler(500)
    def internal_error(e):
        return error_response("Internal server error", "INTERNAL_ERROR", 500)