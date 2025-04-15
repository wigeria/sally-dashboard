""" Contains the model definitions for the database """

from backend.database import db
from backend import settings
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.ext.hybrid import hybrid_property
import uuid


class BaseFieldsMixin:
    """ The Base fields class that all database models are extended from.
        Implements a basic UUID field and DateTime fields for auditing
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                     unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class User(db.Model, BaseFieldsMixin):
    """ Represents the User instance for authentication

        To create a new user:
            user = User(**username_and_email)
            user.password = password  # This hashes the password
            db.session.add(user)
            db.session.commit()

        To verify an existing user's password
            user.verify_password(password)
    """
    __tablename__ = "users"

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(120))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        return check_password_hash(self._password, plaintext)

    def generate_jwt(self):
        """ Generates and returns a JWT token with the user's details in the
            payload
        """
        payload = {
            "uuid": str(self.id),
            "username": self.username,
            "email": self.email,
            # Used internally by jwt.encode for timeout; disabled by
            # `options.verify_exp`
            "exp": datetime.utcnow()+timedelta(seconds=settings.JWT_TIMEOUT)
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @classmethod
    def validate_jwt(cls, token):
        """ Validates that the token refers to a user that exists in the db """
        try:
            decoded = jwt.decode(token.strip(), settings.SECRET_KEY, algorithms="HS256")
            if "uuid" not in decoded:
                raise jwt.exceptions.DecodeError("`UUID` not in segment")
            user = User.query.filter_by(id=decoded["uuid"]).first()
            if not user:
                raise jwt.exceptions.DecodeError("User doesn't exist")
            return user
        except jwt.exceptions.DecodeError:
            return None
        return None


class Bot(db.Model, BaseFieldsMixin):
    """ Represents a SeleniumYAML bot that jobs can be run against """
    __tablename__ = "bots"

    name = db.Column(db.String(80), unique=True, nullable=False)

    @property
    def s3_path(self):
        return f"bots/{self.id}"


class Job(db.Model, BaseFieldsMixin):
    """ Represents a Job against a Bot that is either Running/Finished """
    __tablename__ = "jobs"

    start_time = db.Column(db.DateTime, nullable=False)
    finish_time = db.Column(db.DateTime, nullable=True)
    logs = db.Column(db.Text)
    runtime_data = db.Column(JSON)
    vnc_ws_proxy_port = db.Column(db.Integer, nullable=True, default=None)

    bot_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey(Bot.id), nullable=False)
    bot = db.relationship("Bot", backref=db.backref("jobs", lazy=True))

    @property
    def status(self):
        """ Returns 0 if the bot is still running (no ``finish_time``,
            otherwise 1
        """
        if self.finish_time is None:
            return 0
        return 1
