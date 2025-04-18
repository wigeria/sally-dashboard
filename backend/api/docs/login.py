DOCS = {
    "responses": {
        200: {
            'description': 'Login successful',
            'example': {
                'token': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
                'user': {
                    'id': '123e4567-e89b-12d3-a456-426614174000',
                    'email': 'user@example.com',
                    'username': 'username'
                }
            }
        },
        400: {
            'description': 'Invalid request data',
            'example': {
                'errors': {
                    'email': ['Not a valid email address'],
                    'password': ['Field required']
                }
            }
        },
        401: {
            'description': 'Invalid credentials',
            'example': {
                'error': 'Invalid Credentials'
            }
        }
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