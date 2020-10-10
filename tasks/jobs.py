""" Contains Dramatiq actors for the Bot runs (jobs) """

from backend import settings
from backend.utils import bot_utils
from comm import redis_handler
from contextlib import redirect_stdout
import io
import logging
import os
from selenium import webdriver
import time
# Note that this is loading __init__, which is causing the broker to be set
# properly
from . import dramatiq, settings


os.environ["MOZ_HEADLESS"] = "1"
if os.environ.get("TEST", "False") == "True":
    REDIS_CONF = settings.TEST_REDIS_CONF
else:
    REDIS_CONF = settings.REDIS_CONF


class InterceptionHandler(logging.Handler):
    def __init__(self, *args, job_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_id = job_id

    def emit(self, record):
        message = record.getMessage()
        # TODO: Publish message to `job_id` channel in the broker


def get_driver():
    """ Returns the driver used for running the bots """
    driver = webdriver.Firefox()
    return driver


@dramatiq.actor(max_retries=0)
def run_bot(job_details, runtime_data):
    """ Takes a set of bot details as input, and runs the bot using
        SeleniumYAML

        Parameters
        ----------

        ``job_details`` : dict {
            "id": "job uuid",
            "bot_id": "bot uuid"
            "name": "bot name",
            "s3_path": "bot s3path"
        }

        ``runtime_data`` : dict; data that will be used for templating the
            bot content prior to execution
    """
    # This is all imported inside the worker to keep the logs in
    # separate file-objects per task
    import selenium_yaml
    from loguru import logger

    job_id = job_details["id"]
    bot_id = job_details["bot_id"]
    s3_path = job_details["s3_path"]

    log_file = io.StringIO()
    logger.add(log_file)
    logger.add(InterceptionHandler(job_id=job_id))

    content = bot_utils.download_bot(s3_path)
    print(f"RUNNING: {bot_id}, {content}")

    driver = get_driver()
    engine = selenium_yaml.SeleniumYAML(
        yaml_file=content,
        save_screenshots=False,
        template_context=runtime_data,
        parse_template=bool(runtime_data),
        driver=driver)
    engine.perform(quit_driver=True)

    # Log file now contains all of the logs sent through loguru in the engine
    log_file.seek(0)
    # TODO: Publish success response to redis for ``job_id`` with logs
    channel = redis_handler.CHANNELS["completed_job"]
    r = redis.Redis(**REDIS_CONF)
    r.publish(channel, json.dumps({
        "id": job_id,
        "logs": log_file.getvalue()
    }))
