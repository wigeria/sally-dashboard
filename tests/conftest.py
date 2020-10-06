""" Module containing all of the test fixtures and configuration """

import backend
from backend.database.models import User
import pytest


@pytest.fixture(scope="session")
def client():
    app = backend.create_app(test_config={
        "SQLALCHEMY_DATABASE_URI": backend.settings.TEST_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def db(client):
    """ Fixture for the DB attached to the current session """
    from backend.database import db
    yield db


@pytest.fixture(scope="session")
def user(client, db):
    """ Fixture for a user in the current session's db """
    u = User(email="test@email.com", username="testuser")
    u.password = "testpass"
    db.session.add(u)
    db.session.commit()
    yield u
    db.session.delete(u)
    db.session.commit()
