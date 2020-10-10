""" Contains handler(s) for the Redis Subscriptions """

import backend.database as database
from datetime import datetime
import json
from loguru import logger


@logger.catch()
def job_completed_handler(message):
    """ Handler for the redis subscription on Job completion """
    from .models import Job
    try:
        data = json.loads(message["data"])
        job = Job.query.filter(id=data["id"]).first()
        if not job:
            raise ValueError(
                f"Received completion for job that doesn't exist; `{message}`")

        job.finish_time = datetime.utcnow()
        job.logs = data["logs"]
        database.db.session.commit()
        raise ValueError(f"Job Completed: {message}")
    except:
        # This is done so that the exception gets logged via
        # logger.catch while still skipping any remaining code execution
        raise
