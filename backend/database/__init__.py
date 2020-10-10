""" Package containing Objects and Methods for direct database interactions
    used by the APIs
"""

from backend import settings
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from comm import redis_handler
import backend.database.subscription_handlers as subscription_handlers

db = SQLAlchemy()
migrate = Migrate()
redis = None
subscription_thread = None


def initialize_db(app):
    """ Injects the app into the sqlAlchemy instance """
    app.app_context().push()
    db.init_app(app)
    from . import models
    migrate.init_app(app, db, directory=settings.MIGRATIONS_DIR)
    redis = Redis(**app.config["REDIS_CONF"])
    subscription_thread = redis_handler.create_subscription(
        "completed_jobs", subscription_handlers.job_completed_handler,
        redis)
