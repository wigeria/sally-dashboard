""" Contains Mixins for CRUD Resources for rapid API development """
from backend.database import db


class ListResourceMixin:
    """ Mixin for a LIST API Resource

        Attributes
        ----------

        ``model_class`` - SQLAlchemy Model; Must be set on the class so that
            it can be fetched from the database

        ``serializer_class`` - Marshmallow.Schema; must be set on the class so
            that it can be used for serializing the fetched model instances

        Methods
        -------

        ``get`` - Returns all instances of the ``model_class`` serialized using
            the ``serializer_class``
    """
    def get(self, *args, **kwargs):
        """ Handler for the GET request """
        assert getattr(self, "model_class", None) is not None
        assert getattr(self, "serializer_class", None) is not None

        instances = self.model_class.query.all()
        schema = self.serializer_class(many=True)
        return schema.dump(instances)


class CreateResourceMixin:
    """ Mixin for a CREATE API Resource

        Attributes
        ----------

        ``model_class`` - SQLAlchemy Model; Must be set on the class so that
            it can be acted upon in the database

        ``serializer_class`` - Marshmallow.Schema; must be set on the class so
            that it can be used for serializing the request data

        Methods
        -------

        ``post`` - Creates and adds the model instance to the session after
            validation
    """
    def post(self):
        """ Handler for the POST request """
        assert getattr(self, "model_class", None) is not None
        assert getattr(self, "serializer_class", None) is not None
        pass
