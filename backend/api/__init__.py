""" Package containing the API endpoints for the dashboard """

from flask import Blueprint
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
import os


api = Api()
ma = Marshmallow()
api_bprint = Blueprint("api", __name__)

socketio = SocketIO(logger=True, engineio_logger=True, cors_allowed_origins="*")


def initialize_api(app):
    """ Initializes the API against the provided Flask app """
    REDIS_CONF = app.config["REDIS_CONF"]
    api.init_app(api_bprint)
    ma.init_app(app)
    socketio.init_app(app)
    from . import views, sockets
    app.register_blueprint(api_bprint, url_prefix="/api")
