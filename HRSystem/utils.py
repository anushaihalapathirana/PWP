"""
This file contains the util functions
"""
from flask import abort

def create_error_message(status_code, error, message=None):
    """
    Method to create error message
    Return
        -error object
    """
    error_message = {
        'Code': status_code,
        'Error': error,
        'Message': message
        }
    return abort(status_code, error_message)
