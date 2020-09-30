""" Contains tests for the views declared in the Backend.app instance """

import os
os.environ["TESTING"] = "True"


from flask import Flask
import pytest
from backend.database import initialize_db
from backend import settings


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = None
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True

    with app.test_client() as client:
        initialize_db(app)
        yield client


def test_empty_db(client):
    raise ValueError("Client", client)