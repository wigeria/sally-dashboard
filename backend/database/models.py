""" Contains the model definitions for the database """

from backend.database import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSON
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
    """ Represents the User instance for authentication """
    __tablename__ = "users"

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


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
    runtime_date = db.Column(JSON)

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
    
