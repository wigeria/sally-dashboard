""" Flask App setting up all of the base dependencies + importing in
    other dependencies
"""

from flask import Flask
from backend.database import initialize_db, db
from backend.api import initialize_api
import os
import backend.settings
import sys


def create_app(test_config=None):
    """ Creates and configures and the app and it's dependencies """
    app = Flask(__name__)

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    else:
        app.config.from_mapping(test_config)

    initialize_db(app)
    initialize_api(app)

    return app
