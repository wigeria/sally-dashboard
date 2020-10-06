""" Contains decorators used across the API Resources """

from backend.database.models import User
from flask import request
from functools import wraps


def is_authenticated(func):
    """ Decorator for validating a JWT Token """
    prefix = "Token"
    error = {
        "error": "Unauthorized"
    }, 401
    @wraps(func)
    def wrapper(*args, **kwargs):
        header = str(request.headers.get("Authorization"))
        token = header.split(prefix)[-1].strip()
        if not token:
            return error
        user = User.validate_jwt(token)
        if user:
            return func(*args, user=user, **kwargs)
        return error
    return wrapper
