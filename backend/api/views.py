""" Contains the API Views resources for each endpoint """

from . import api
from .decorators import is_authenticated
from .mixins import ListResourceMixin, CreateResourceMixin
from .request_schemas import UserLoginRequestSchema
from .serializers import BotsSchema
from backend.database.models import Bot, User
from flask import request, jsonify, make_response
from flask_restful import Resource
from marshmallow import ValidationError


class TestResource(Resource):
    def get(self):
        return {'status': 'Running'}
api.add_resource(TestResource, '/')


class LoginResource(Resource):
    """ Endpoint for validating user credentials and generating a JWT Token """
    def post(self):
        """ Attempts to log the user in after validating creds """
        body = request.stream.read()
        schema = UserLoginRequestSchema()
        try:
            data = schema.loads(json_data=body)
        except ValidationError as err:
            errors = err.messages
            return make_response(jsonify(errors=errors), 400)

        user = User.query.filter(User.email == data["email"]).first()
        if not user:
            return make_response(jsonify({
                "error": "Invalid Credentials"
            }), 401)
        if not user.verify_password(data["password"]):
            return make_response(jsonify({
                "error": "Invalid Credentials"
            }), 401)

        response = {
            "token": user.generate_jwt().decode(),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username
            }
        }
        return make_response(jsonify(response), 200)
api.add_resource(LoginResource, "/login/")


class BotsResource(Resource, ListResourceMixin, CreateResourceMixin):
    model_class = Bot
    serializer_class = BotsSchema