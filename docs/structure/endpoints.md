# Endpoints
-----------

These are the endpoints offered by the REST API

### Login

URL: `/api/login/`

Method: `POST`

Request Body:
```json
    {
        "email": "email",
        "password": "password"
    }
```

Response:
```json
    {
        "token": "JWT Token", 
        "user": {
            "...": "user details"
        }
    }
```

The token in the response can be used in the `Authorization: Token <token>` header for authentication.


### Bots List

URL: `/api/bots/`

Response:
```json
    [
        {
            "uuid": "bot uuid",
            "name": "bot name"
        }
    ]
```

### Bot Creation

URL: `/api/bots/`

Method: `POST`

Request Body:
```json
    {
        "name": "bot name",
        "file": "yaml file object"
    }
```

Response:

1. 201
```json
    {
        "uuid": "UUID",
        "name": "bot name",
        "file": "YAML Download link"
    }
```
2. 400
```json
    {
        "errors": ["list of errors"]
    }
```

### Bot Delete

URL: `/api/bots/:botUUID`

Method: `DELETE`

### Bots Detail

URL: `/api/bots/:botUUID`

Method: `GET`

Response:
```json
    {
        "uuid": "UUID",
        "name": "Bot Name",
        "fields": { bot Jinja fields }
    }
```

### List Jobs

URL: `/api/jobs/`

Response:
```json
    [
        {
            "uuid": "UUID",
            "bot": {
                "uuid": "UUID",
                "name": "Bot Name"
            },
            "-- Other job details"
        }
    ]
```

### Start Jobs

URL: `/api/jobs/`

Method: `POST`

Request Body:
```json
    {
        "bot_id": "Bot UUID",
        "runtime_data": {
            "template_variable": "values"
        }
    }
```

Response:
```json
    {
        "job_id": "UUID",
        "status": "Running"
    }
```

### Jobs Detail

URL: `/api/jobs/:jobUUID/`

Method: `GET`

Parameters

- `status` - 0: Running Jobs, 1: Finished Jobs

Response:
```json
    {
        "job_id": "UUID",
        "start_time": "",
        "finish_time": "",
        "runtime_data": "",
        "logs": "",
        "bot": {}
    }
```
