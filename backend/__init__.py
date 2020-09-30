""" Flask App setting up all of the base dependencies + importing in
    other dependencies
"""

from flask import Flask
from backend.database import initialize_db, db
import os
import backend.settings
import sys


if not os.environ.get("TESTING", "False") == "True":
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    initialize_db(app)
