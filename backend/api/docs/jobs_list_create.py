import backend.api as api
from flask_restx import fields


ERROR_MESSAGE = api.api.model('jobs_list_ErrorMessage', {
    'error': fields.String(example='Invalid Data')
})
BOT_INFO = api.api.model('jobs_BotInfo', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'name': fields.String(example='My Bot')
})
JOB_DETAIL = api.api.model('jobs_JobDetail', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'start_time': fields.DateTime(example='2023-01-01T00:00:00Z'),
    'finish_time': fields.DateTime(example='2023-01-01T00:01:00Z'),
    'status': fields.String(example='completed'),
    'result': fields.Raw(example={
        'success': True,
        'message': 'Job completed successfully'
    }),
    'runtime_data': fields.Raw(example={
        'username': 'testuser',
        'password': '********'
    }),
    'bot': fields.Nested(BOT_INFO)
})
CREATE_JOB_REQUEST = api.api.model('jobs_CreateJobRequest', {
    'bot_id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'runtime_data': fields.Raw(example={
        'username': 'testuser',
        'password': 'password123'
    })
})

DOCS = {
    'get': {
        'responses': {
            200: api.api.model('jobs_ListResponse', {
                'items': fields.List(fields.Nested(JOB_DETAIL)),
                'total': fields.Integer(example=10)
            }),
            401: ERROR_MESSAGE
        },
        'params': {}
    },
    'post': {
        'responses': {
            201: JOB_DETAIL,
            400: ERROR_MESSAGE,
            401: ERROR_MESSAGE,
            404: api.api.model('jobs_NotFoundError', {
                'error': fields.String(example='Bot Does Not Exist')
            })
        },
        'params': {},
        'request_model': CREATE_JOB_REQUEST
    }
}
