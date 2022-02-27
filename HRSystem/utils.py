
from flask import abort

def create_error_message(status_code, error, message=None):

    error_message = {
        'Code': status_code,
        'Error': error,
        'Message': message
        }
    return abort(status_code, error_message)