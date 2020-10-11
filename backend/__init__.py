""" Flask App setting up all of the base dependencies + importing in
    other dependencies
"""

from flask import Flask
from backend.database import initialize_db, db
from backend.api import initialize_api
import os
import backend.settings as settings
import sys


def create_app():
    """ Creates and configures and the app and it's dependencies """
    app = Flask(__name__)

    test_config = None
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["REDIS_CONF"] = settings.REDIS_CONF

    initialize_db(app)
    initialize_api(app)

    @app.after_request
    def after_request(response):
        """ Adding CORS headers into response """
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app


if __name__ == "__main__":
    from backend import api, settings
    from flask_socketio import SocketIO

    app = create_app()
    api.socketio.run(app, host=settings.HOST, port=int(settings.PORT))
