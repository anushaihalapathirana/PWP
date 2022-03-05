"""
This file contains the util functions
"""
import secrets
from flask import abort
from HRSystem.models import ApiKey

def create_error_message(status_code, error, message=None):
    """
    Method to create error message
    Return
        - Error object
    """
    error_message = {
        'Code': status_code,
        'Error': error,
        'Message': message
        }
    return abort(status_code, error_message)

def require_admin(func):
    """
    Method to validate admin key
    """
    def wrapper(*args, **kwargs):
        key_hash = ApiKey.key_hash(request.headers.get("HRSystem-Api-Key").strip())
        db_key = ApiKey.query.filter_by(admin=True).first()
        if secrets.compare_digest(key_hash, db_key.key):
            return func(*args, **kwargs)
        raise Forbidden
    return wrapper

def require_employee_key(func):
    """
    Method to validate employee key
    """
    def wrapper(self, sensor, *args, **kwargs):
        key_hash = ApiKey.key_hash(request.headers.get("HRSystem-Api-Key").strip())
        db_key = ApiKey.query.filter_by(sensor=sensor).first()
        if db_key is not None and secrets.compare_digest(key_hash, db_key.key):
            return func(*args, **kwargs)
        raise Forbidden
    return wrapper
