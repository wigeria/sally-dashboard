# Outline
---------

The project is based around three major components.

- Backend

- Frontend

- Queued Tasks

## Backend

The backend is built using Python 3 with the Flask framework. It revolves around using a PostgreSQL database for storing relational Bot data and a Redis database for acting as a message broker and task queue through the [Dramatiq](https://dramatiq.io/) Task Processing library.

The backend and the tasks queue/worker(s) will be in a single container running in separate processes. Perhaps use supervisor for this. The tasks also communicate with the main flask process through a socket interface.

The business model would be to serve this dashboard as a standalone set of docker-compose managed images, and after implementing a system for upload "plugins" (identified as python packages), create a dashboard for selling those plugins and other services such as hosting etc.

**Note: For Docker; use `host.docker.internal` for windows Postgres DB, and `--net=host` combined with `127.0.0.1` for DB Host for unix**

### File Structure

```
backend/
	__init__.py - App and base flask methods
	settings.py - Configuration details
	db/
		__init__.py - DB Declaration
		models.py - Models Declaration
	api/
		__init__.py - API Framework Declaration
		views.py - API Endpoints through the Framework
	logging/
		__init__.py - Logger Declaration (loguru?)
		utils.py - Helper methods for logs (?) ; if not required, this might just be a module instead of a package
```

### Models

These are the models stored within the databases, along with details on what they represent. The user's model will be fairly generic (with an added UUID field), so it isn't mentioned below).

All of the models have the following fields:

```
id UUID
created_at Datetime
updated_at Datetime
```

#### Bots

The Bots are stored in a SQL table with a schema as follows:

```
name Varchar(255) Distinct
jobs Backref Jobs FK
```

The most important of those fields, the `bot` field, contains an S3 filepath for the SeleniumYAML bot that the particular row will represent. At the moment, this file isn't encrypted, but encryption will be implemented in the future.

Before the file is uploaded, it is validated using the SeleniumYAML engine to confirm the schema.

The model also has a `s3_path` property that returns `bots/:id`

#### Jobs

The Jobs are stored in a SQL table with a schema as follows:

```
bot_id UUID Foreign
start_time DateTime
finish_time DateTime AllowNull
logs Text
runtime_data JSON
```

While the Job is running, it is also stored in Redis namespaced under the User's UUID as follows:

```
{
	"job_id": int,
	"runtime_data": {
		"data provided": "by the user for the runtime (template variables etc.)"
	},
	"bot_path": "path to the bot in s3",
	"logs": "a constant stream that all bot logs are piped to"
}
```

While the bot is running, a Session is established between the Frontend and the Backend along with a Pub/Sub connection between the Backend and the Task queues. As data comes in from the Queue to the Backend, it is sent along to the Frontend through the Socket (logs etc.) as well as logged into the SQL Job's row. At a time, the user should only be connected to a single bot's socket at a time.

After the bot has finished running, it is removed from Redis, and all logs are simply presented to the user through the SQL table and the socket is no longer in use.

The Jobs model also has a `status` property that returns `0` if the finish time is null (unfinished job) or `1` otherwise.
