from flask import jsonify

def success_response(data=None, message="Operation successful", status_code=200):
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message="An error occurred", error_code="INTERNAL_ERROR", status_code=500):
    response = {
        "success": False,
        "message": message,
        "error": error_code
    }
    return jsonify(response), status_code