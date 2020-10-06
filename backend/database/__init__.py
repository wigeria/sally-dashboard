""" Package containing Objects and Methods for direct database interactions
    used by the APIs
"""

from backend import settings
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def initialize_db(app):
    """ Injects the app into the sqlAlchemy instance """
    app.app_context().push()
    db.init_app(app)
    from . import models
    migrate.init_app(app, db, directory=settings.MIGRATIONS_DIR)
