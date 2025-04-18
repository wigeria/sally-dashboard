import backend.api as api
from flask_restx import fields


ERROR_MESSAGE = api.api.model('login_ErrorMessage', {
    'error': fields.String,
})
VALIDATION_ERRORS = api.api.model('login_ValidationErrors', {
    'errors': fields.Raw(example={
        'email': ['Not a valid email address'],
        'password': ['Field required']
    })
})
USER = api.api.model('login_User', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'email': fields.String(example='user@example.com'),
    'username': fields.String(example='username')
})
LOGIN_RESPONSE = api.api.model('login_LoginResponse', {
    'token': fields.String(example='eyJ0eXAiOiJKV1QiLCJhbGc...'),
    'user': fields.Nested(USER)
})


DOCS = {
    "responses": {
        200: LOGIN_RESPONSE,
        400: VALIDATION_ERRORS,
        401: ERROR_MESSAGE,
    },
    "params": {
        'email': {
            'in': 'body',
            'description': 'User email address',
            'required': True,
            'type': 'string',
            'example': 'user@example.com'
        },
        'password': {
            'in': 'body',
            'description': 'User password',
            'required': True,
            'type': 'string',
            'example': 'password123'
        }
    },
}