""" Contains Marshmallow Schemas used by the APIs """

from . import ma
from backend.database.models import User, Bot
from marshmallow import validate


class UsersSchema(ma.SQLAlchemyAutoSchema):
    """ Auto-generated Schema for the User models """
    class Meta:
        model = User
        include_fk = True


class BotsSchema(ma.SQLAlchemyAutoSchema):
    """ Auto-generated Schema for the Bot model """
    class Meta:
        model = Bot
