""" Contains Marshmallow Schemas used by the APIs """

from . import ma
from backend.database.models import User, Bot, Job
import backend.utils.bot_utils as bot_utils
from jinja2 import Environment, meta
from marshmallow import validate
from marshmallow import fields as ma_fields


class UsersSchema(ma.SQLAlchemyAutoSchema):
    """ Auto-generated Schema for the User models """
    class Meta:
        model = User
        include_fk = True


class BotsSchema(ma.SQLAlchemyAutoSchema):
    """ Auto-generated Schema for the Bot model """
    class Meta:
        model = Bot


class BotsDetailSchema(ma.SQLAlchemyAutoSchema):
    """ Auto-generated Schema for the Bot model with additional details """
    fields = ma_fields.Method("get_fields")

    def get_fields(self, instance):
        """ Returns Jinja fields from the bot's YAML """
        bot_yaml = bot_utils.download_bot(instance.s3_path)
        env = Environment()
        template = env.parse(bot_yaml)
        return list(meta.find_undeclared_variables(template))

    class Meta:
        model = Bot
        fields = ["id", "name", "fields"]


class JobsSchema(ma.SQLAlchemyAutoSchema):
    """ Auto-generated Schema for the Jobs model with a nested Bot """
    bot = ma.Nested(BotsSchema)

    class Meta:
        model = Job
        include_fk = True
