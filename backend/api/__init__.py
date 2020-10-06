""" Package containing the API endpoints for the dashboard """

from flask import Blueprint
from flask_restful import Api
from flask_marshmallow import Marshmallow


api = Api()
ma = Marshmallow()
api_bprint = Blueprint("api", __name__)

def initialize_api(app):
    """ Initializes the API against the provided Flask app """
    api.init_app(api_bprint)
    ma.init_app(app)
    from . import views
    app.register_blueprint(api_bprint, url_prefix="/api")
