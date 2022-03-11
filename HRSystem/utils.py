"""
This file contains the util functions
"""
import secrets
from flask import abort, request
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
        apiKey = request.headers.get("HRSystem-Api-Key")
        if apiKey is None:
            raise abort(403)
        key_hash = ApiKey.key_hash(
            request.headers.get("HRSystem-Api-Key").strip())
        db_key = ApiKey.query.filter_by(admin=True).first()
        if secrets.compare_digest(key_hash, db_key.key):
            return func(*args, **kwargs)
        raise abort(403)
    return wrapper


def require_employee_key(func):
    """
    Method to validate employee key
    """

    def wrapper(self, employee, *args, **kwargs):
        apiKey = request.headers.get("HRSystem-Api-Key")
        if apiKey is None:
            raise abort(403)
        key_hash = ApiKey.key_hash(
            request.headers.get("HRSystem-Api-Key").strip())
        admin_db_key = ApiKey.query.filter_by(admin=True).first()
        if secrets.compare_digest(key_hash, admin_db_key.key):
            return func(self, employee, *args, **kwargs)
        else:
            db_key = ApiKey.query.filter_by(employee=employee).first()
            if db_key is not None and secrets.compare_digest(key_hash, db_key.key):
                return func(self, employee, *args, **kwargs)
            raise abort(403)

    return wrapper
