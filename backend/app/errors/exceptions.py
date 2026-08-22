class APIError(Exception):
    def __init__(self, message, error_code, status_code=400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)