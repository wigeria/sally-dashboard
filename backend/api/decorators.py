""" Contains decorators used across the API Resources """

from backend.database.models import User
from flask import request
from functools import wraps
import jwt


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
        try:
            user = User.validate_jwt(token)
        except jwt.exceptions.ExpiredSignatureError:
            return error
        if user:
            return func(*args, user=user, **kwargs)
        return error
    return wrapper
