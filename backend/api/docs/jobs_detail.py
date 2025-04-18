import backend.api as api
from flask_restx import fields

ERROR_MESSAGE = api.api.model('jobs_detail_ErrorMessage', {
    'error': fields.String(example='Does Not Exist')
})

BOT_INFO = api.api.model('jobs_detail_BotInfo', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'name': fields.String(example='My Bot')
})

JOB_DETAIL = api.api.model('jobs_detail_JobDetail', {
    'id': fields.String(example='123e4567-e89b-12d3-a456-426614174000'),
    'start_time': fields.DateTime(example='2023-01-01T00:00:00Z'),
    'finish_time': fields.DateTime(example='2023-01-01T00:01:00Z'),
    'runtime_data': fields.Raw(example={
        'username': 'testuser',
        'password': '********',
        'target_url': 'https://example.com'
    }),
    'logs': fields.String(example='...'),
    'bot': fields.Nested(BOT_INFO)
})

DOCS = {
    'get': {
        'responses': {
            200: JOB_DETAIL,
            404: ERROR_MESSAGE,
            401: ERROR_MESSAGE
        },
        'params': {
            'job_id': {
                'in': 'path',
                'description': 'ID of the job to retrieve',
                'required': True,
                'type': 'string',
                'example': '123e4567-e89b-12d3-a456-426614174000'
            }
        }
    }
}