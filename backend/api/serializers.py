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
    bot_content = ma_fields.Method("get_bot_content")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_bot_yaml = {}

    def _get_bot_yaml(self, instance):
        """ Returns cached bot YAML or downloads it if not cached """
        if instance.id not in self._cached_bot_yaml:
            self._cached_bot_yaml[instance.id] = bot_utils.download_bot(instance.s3_path)
        return self._cached_bot_yaml[instance.id]

    def get_fields(self, instance):
        """ Returns Jinja fields from the bot's YAML """
        bot_yaml = self._get_bot_yaml(instance)
        env = Environment()
        template = env.parse(bot_yaml)
        return list(meta.find_undeclared_variables(template))

    def get_bot_content(self, instance):
        """ Returns the content of the bot's YAML file from S3 """
        return self._get_bot_yaml(instance)

    class Meta:
        model = Bot
        fields = ["id", "name", "fields", "bot_content"]


class JobsSchema(ma.SQLAlchemyAutoSchema):
    """ Auto-generated Schema for the Jobs model with a nested Bot """

    bot = ma.Nested(BotsSchema)

    class Meta:
        model = Job
        include_fk = True
