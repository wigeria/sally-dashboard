import backend.api as api
from flask_restx import fields


ERROR_MESSAGE = api.api.model('bots_retrieve_ErrorMessage', {
    'error': fields.String(example='Does Not Exist')
})
DELETE_SUCCESS = api.api.model('bots_delete_Success', {
    'message': fields.String(example='Deleted')
})
VALIDATION_ERRORS = api.api.model('bots_detail_ValidationErrors', {
    'errors': fields.Raw(example={
        'assertion': 'Invalid YAML structure',
        'name': 'name must be <= 80 characters'
    })
})
BOT_DETAIL = api.api.model('bots_BotDetail', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'name': fields.String(example='My Bot'),
    'created': fields.DateTime(example='2023-01-01T00:00:00Z'),
    'jinja_fields': fields.Raw(example={
        'username': 'Username field',
        'password': 'Password field'
    })
})
BOT_UPDATE = api.api.model('bots_BotUpdate', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'name': fields.String(example='Updated Bot Name')
})

DOCS = {
    'get': {
        'responses': {
            200: BOT_DETAIL,
            404: ERROR_MESSAGE,
            401: ERROR_MESSAGE
        },
        'params': {
            'bot_id': {
                'in': 'path',
                'description': 'ID of the bot to retrieve',
                'required': True,
                'type': 'string',
                'example': '123e4567-e89b-12d3-a456-426614174000'
            }
        }
    },
    'delete': {
        'responses': {
            200: DELETE_SUCCESS,
            404: ERROR_MESSAGE,
            401: ERROR_MESSAGE
        },
        'params': {
            'bot_id': {
                'in': 'path',
                'description': 'ID of the bot to delete',
                'required': True,
                'type': 'string',
                'example': '123e4567-e89b-12d3-a456-426614174000'
            }
        }
    },
    'patch': {
        'responses': {
            200: BOT_UPDATE,
            400: VALIDATION_ERRORS,
            404: ERROR_MESSAGE,
            401: ERROR_MESSAGE
        },
        'params': {
            'bot_id': {
                'in': 'path',
                'description': 'ID of the bot to update',
                'required': True,
                'type': 'string',
                'example': '123e4567-e89b-12d3-a456-426614174000'
            },
            'file': {
                'in': 'formData',
                'description': 'Updated YAML file for the bot',
                'required': False,
                'type': 'file'
            },
            'name': {
                'in': 'formData',
                'description': 'New name for the bot',
                'required': False,
                'type': 'string',
                'example': 'Updated Bot Name'
            }
        }
    }
}