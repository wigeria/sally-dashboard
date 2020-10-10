""" Contains the API Views resources for each endpoint """

from . import api
from .decorators import is_authenticated
from .mixins import ListResourceMixin, CreateResourceMixin
from .request_schemas import UserLoginRequestSchema
from .serializers import BotsSchema, JobsSchema
from backend.database import db
from backend.database.models import Bot, User, Job
from backend.utils import bot_utils
from datetime import datetime
from flask import request, jsonify, make_response, escape
from flask_restful import Resource, reqparse
import json
from marshmallow import ValidationError
import selenium_yaml
import sqlalchemy
from sqlalchemy.orm import joinedload
from tasks import jobs
import werkzeug


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


class BotsListCreateResource(Resource, ListResourceMixin):
    model_class = Bot
    serializer_class = BotsSchema
    method_decorators = [is_authenticated]

    def post(self, user=None):
        """ Creates a Bot instance by first validating the provided file
            and then uploading it to S3
        """
        if "file" not in request.files or "name" not in request.form:
            return make_response(jsonify({
                "errors": "Missing file/name"
            }), 400)
        if len(request.form["name"]) > 80 or len(request.form["name"]) < 1:
            return make_response(jsonify({
                "errors": "``name`` <= 80"
            }), 400)
        yaml_content = request.files["file"].read()
        try:
            bot_utils.parse_yaml_bot(yaml_content)
        except selenium_yaml.exceptions.ValidationError as err:
            return make_response(jsonify({
                "errors": err.error
            }), 400)
        except AssertionError as err:
            return make_response(jsonify({
                "errors": {"assertion": err.args[0]}
            }), 400)

        bot = Bot(name=escape(request.form["name"]))
        db.session.add(bot)
        db.session.commit()
        bot_utils.upload_bot(yaml_content, bot.s3_path)
        return make_response(jsonify({
            "id": str(bot.id),
            "name": bot.name
        }), 201)
api.add_resource(BotsListCreateResource, "/bots/")


class BotsDeleteResource(Resource):
    """ Resource implementing endpoints for deleting Bots """
    method_decorators = [is_authenticated]

    def delete(self, bot_id, user=None):
        """ Deletes the given Bot as well as it's file from S3 """
        bot = Bot.query.filter(Bot.id == bot_id).first()
        if not bot:
            return make_response(jsonify({
                "error": "Does Not Exist"
            }), 404)
        bot_utils.delete_bot(bot.s3_path)
        Job.query.filter(Job.bot_id == bot.id).delete()
        db.session.delete(bot)
        db.session.commit()
        return make_response(jsonify({
            "message": "Deleted"
        }), 200)
api.add_resource(BotsDeleteResource, "/bots/<string:bot_id>/")


class JobsListCreateResource(ListResourceMixin, Resource):
    """ Resource for listing/creating new jobs """
    method_decorators = [is_authenticated]
    model_class = Job
    serializer_class = JobsSchema

    def get_queryset(self):
        """ Overwritten to add support for filtering by status """
        filters = []
        status = request.args.get("status", None)
        if status == "0":
            filters.append(Job.finish_time == None)
        elif status == "1":
            filters.append(Job.finish_time != None)
        return self.model_class.query.filter(*filters) \
            .options(joinedload(Job.bot))

    def post(self, user=None):
        """ Creates and starts a new job against a given bot """
        data = request.get_json()
        if "bot_id" not in data or "runtime_data" not in data or not \
                isinstance(data["runtime_data"], dict):
            return make_response(jsonify({
                "error": "Invalid Data"
            }), 400)

        bot_id = data["bot_id"]
        try:
            bot = Bot.query.filter(Bot.id == bot_id).first()
        except sqlalchemy.exc.DataError:
            db.session.rollback()
            bot = None
        if not bot:
            return make_response(jsonify({
                "error": "Bot Does Not Exist"
            }), 404)

        job = Job(
            start_time=datetime.utcnow(),
            runtime_data=json.dumps(data["runtime_data"]),
            bot_id=bot.id)
        db.session.add(job)
        db.session.commit()
        jobs.run_bot.send({
            "id": str(job.id),
            "bot_id": str(bot.id),
            "name": bot.name,
            "s3_path": bot.s3_path
        }, data["runtime_data"])
        schema = self.serializer_class()
        return make_response(jsonify(schema.dump(job)), 201)
api.add_resource(JobsListCreateResource, "/jobs/")


class JobsDetailResource(Resource):
    """ Resource implementing endpoints for get a single Job's Details """
    method_decorators = [is_authenticated]
    serializer_class = JobsSchema

    def get(self, job_id, user=None):
        """ Returns details for the given job """
        job = Job.query.filter(Job.id == job_id).first()
        if not job:
            return make_response(jsonify({
                "error": "Does Not Exist"
            }), 404)
        schema = self.serializer_class()
        return make_response(jsonify(schema.dump(job)), 200)
api.add_resource(JobsDetailResource, "/jobs/<string:job_id>/")
