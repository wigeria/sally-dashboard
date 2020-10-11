""" Module containing all of the test fixtures and configuration """

import backend
import pytest
import os


os.environ["TEST"] = "True"


@pytest.fixture(scope="session")
def client():
    os.environ["TEST"] = "True"
    app = backend.create_app()

    with app.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def db(client):
    """ Fixture for the DB attached to the current session """
    from backend.database import db
    from backend.database.models import User, Bot, Job
    User.query.delete()
    Job.query.delete()
    Bot.query.delete()
    yield db


@pytest.fixture(scope="session")
def user(client, db):
    """ Fixture for a user in the current session's db """
    from backend.database.models import User
    u = User(email="test@email.com", username="testuser")
    u.password = "testpass"
    db.session.add(u)
    db.session.commit()
    yield u
    db.session.delete(u)
    db.session.commit()
