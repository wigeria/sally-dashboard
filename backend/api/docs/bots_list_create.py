import backend.api as api
from flask_restx import fields


# Common Models
ERROR_MESSAGE = api.api.model('bots_ErrorMessage', {
    'errors': fields.String(example='Missing file/name')
})
VALIDATION_ERROR = api.api.model('bots_ValidationError', {
    'errors': fields.Raw(example={
        'assertion': 'Invalid bot configuration'
    })
})
BOT = api.api.model('Bot', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'name': fields.String(example='My Bot')
})
# Documentation for both endpoints
DOCS = {
    'get': {
        'responses': {
            200: fields.List(fields.Nested(BOT)),
            401: ERROR_MESSAGE,
        },
        'params': {}
    },
    'post': {
        'responses': {
            201: BOT,
            400: ERROR_MESSAGE,
            401: ERROR_MESSAGE
        },
        'params': {
            'file': {
                'in': 'formData',
                'description': 'YAML file containing bot configuration',
                'required': True,
                'type': 'file'
            },
            'name': {
                'in': 'formData',
                'description': 'Name of the bot (1-80 characters)',
                'required': True,
                'type': 'string',
                'example': 'My Bot'
            }
        },
        'consumes': ['multipart/form-data']
    }
}