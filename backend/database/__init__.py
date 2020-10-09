""" Package containing Objects and Methods for direct database interactions
    used by the APIs
"""

from backend import settings
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis


db = SQLAlchemy()
migrate = Migrate()
redis = None


def initialize_db(app):
    """ Injects the app into the sqlAlchemy instance """
    app.app_context().push()
    db.init_app(app)
    from . import models
    migrate.init_app(app, db, directory=settings.MIGRATIONS_DIR)
    redis = Redis(**app.config["REDIS_CONF"])
