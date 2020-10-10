""" Flask App setting up all of the base dependencies + importing in
    other dependencies
"""

from flask import Flask
from backend.database import initialize_db, db
from backend.api import initialize_api
import os
import backend.settings
from dramatiq.brokers.redis import RedisBroker
import redis
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

    app.config["DRAMATIQ_BROKER"] = RedisBroker
    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["REDIS_CONF"] = settings.REDIS_CONF
        app.config["DRAMATIQ_BROKER_URL"] = \
            f"redis://{settings.REDIS_CONF['host']}:{settings.REDIS_CONF['port']}"
    else:
        app.config.from_mapping(test_config)
        app.config["REDIS_CONF"] = settings.TEST_REDIS_CONF
        app.config["DRAMATIQ_BROKER_URL"] = \
            f"redis://{settings.TEST_REDIS_CONF['host']}:" + \
            f"{settings.TEST_REDIS_CONF['port']}"

    initialize_db(app)
    initialize_api(app)

    return app
