""" Contains Dramatiq actors for the Bot runs (jobs) """

from backend import settings
from backend.utils import bot_utils
from contextlib import redirect_stdout
import io
import logging
import os
from selenium import webdriver
import time
# Note that this is loading __init__, which is causing the broker to be set
# properly
from . import dramatiq


os.environ["MOZ_HEADLESS"] = "1"


class InterceptionHandler(logging.Handler):
    def __init__(self, *args, bot_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_id = bot_id

    def emit(self, record):
        message = record.getMessage()
        print(f"NEW LOG for `{self.bot_id}`: {record.getMessage()}")
        # TODO: Publish message to `bot_id` channel in the broker


def get_driver():
    """ Returns the driver used for running the bots """
    driver = webdriver.Firefox()
    return driver


@dramatiq.actor(max_retries=0)
def run_bot(bot_details, runtime_data):
    """ Takes a set of bot details as input, and runs the bot using
        SeleniumYAML

        Parameters
        ----------

        ``bot_details`` : dict {
            "id": "bot uuid",
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
    log_file = io.StringIO()
    logger.add(log_file)
    logger.add(InterceptionHandler(bot_id=bot_details["id"]))

    content = bot_utils.download_bot(bot_details["s3_path"])
    print(f"RUNNING: {bot_details['id']}, {content}")

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
    # TODO: Publish success response to redis for ``bot_id`` with logs
    print(f"LOGS: {log_file.getvalue()}")
