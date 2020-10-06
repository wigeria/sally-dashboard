""" Contains the schemas used for validating requests """
from . import ma
from marshmallow import validate


class UserLoginRequestSchema(ma.Schema):
    """ Schema used for validating the login request body """
    email = ma.Email(required=True)
    password = ma.String(
        required=True, validate=validate.Length(min=1, max=120))