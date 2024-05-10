""" Contains Dramatiq actors for the Bot runs (jobs) """

from contextlib import redirect_stdout
from datetime import datetime
import io
import importlib
import json
from flask import Flask
import logging
import os
from selenium import webdriver
import socketio
import time
# Note that this is loading __init__, which is causing the broker to be set
# properly
from . import dramatiq, settings, DISTRIBUTED_MUTEX
from plugins import *
from pyvirtualdisplay import Display


# os.environ["MOZ_HEADLESS"] = "1"


def emit_job_message(socket, message):
    """ General handler for emitting any messages to the socket """
    socket.emit(
        'job_update',
        message,
        namespace='/'
    )

class InterceptionHandler(logging.Handler):
    def __init__(self, *args, job_id=None, socket=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_id = job_id
        self.socket = socket

    def emit(self, record):
        message = record.getMessage()
        emit_job_message(self.socket, {"id": self.job_id, "log": message})
        # TODO: Publish message to `job_id` channel in the broker


def get_driver(*args, **kwargs):
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
    from backend.utils import bot_utils
    from backend.database import db
    from backend.database.models import Job
    import selenium_yaml
    from loguru import logger

    with DISTRIBUTED_MUTEX.acquire():
        job_id = job_details["id"]
        bot_id = job_details["bot_id"]
        s3_path = job_details["s3_path"]
        sio = socketio.Client()
        sio.connect(
            settings.WS_URL+f"?secret={settings.WS_SECRET}", namespaces=["/jobs"])

        log_file = io.StringIO()
        logger.add(log_file)
        logger.add(InterceptionHandler(job_id=job_id, socket=sio))

        content = bot_utils.download_bot(s3_path).decode()
        print(f"RUNNING: {bot_id}")

        if settings.SELENIUM_DRIVER_INITIALIZER is not None:
            mod_name, func_name = settings.SELENIUM_DRIVER_INITIALIZER.rsplit('.', 1)
            package = importlib.import_module(mod_name)
            get_driver = getattr(package, func_name)

        with Display() as display:
            driver = get_driver(
                job_details=job_details, runtime_data=runtime_data)
            try:
                engine = selenium_yaml.SeleniumYAML(
                    yaml_file=content,
                    save_screenshots=False,
                    template_context=runtime_data,
                    parse_template=bool(runtime_data),
                    driver=driver)
                engine.perform(quit_driver=True, dynamic_delay_range=(0.5, 2))
            except:
                if engine.driver is not None:
                    engine.driver.quit()
                    engine.driver = None

        # Log file now contains all of the logs sent through loguru in the engine
        log_file.seek(0)
        finish_time = datetime.utcnow()

        emit_job_message(
            sio,
            {
                "id": job_id,
                "log": "-- Finished --",
                "finish_time": finish_time.isoformat()
            })

        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        with app.app_context():
            job = Job.query.filter(Job.id == job_id).first()
            if not job:
                raise ValueError(
                    f"Received completion for job that doesn't exist; `{message}`")

            job.finish_time = finish_time
            job.logs = log_file.getvalue()
            db.session.commit()
        sio.disconnect()
