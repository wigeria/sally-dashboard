""" Flask App setting up all of the base dependencies + importing in
    other dependencies
"""

from flask import Flask
from backend.database import initialize_db, db
from backend.api import initialize_api
import os
import backend.settings
import sys


TEST_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": settings.TEST_DATABASE_URI,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}


def create_app():
    """ Creates and configures and the app and it's dependencies """
    app = Flask(__name__)

    test_config = None
    if os.environ.get("TEST", "false") == "True":
        test_config = TEST_CONFIG
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    else:
        app.config.from_mapping(test_config)

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
