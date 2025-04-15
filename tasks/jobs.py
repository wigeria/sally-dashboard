""" Contains Dramatiq actors for the Bot runs (jobs) """

from contextlib import redirect_stdout
from datetime import datetime
from backend.database.models import Job
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
import subprocess
import websockify
from multiprocessing import Process


def run_websockify(websockify_port, rfb_port):
    websockify_server = websockify.WebSocketProxy(
        listen_port=websockify_port,
        target_host='localhost',
        target_port=rfb_port,
        daemon=False,
    )
    websockify_server.start_server()

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
    from tasks import task_utils
    import selenium_yaml # type: ignore
    from loguru import logger

    with DISTRIBUTED_MUTEX.acquire(), task_utils.TaskContextManager() as db:
        job_id = job_details["id"]
        bot_id = job_details["bot_id"]
        s3_path = job_details["s3_path"]

        # Getting the job being executed
        job = Job.query.filter(Job.id == job_id).first()
        sio = socketio.Client()
        sio.connect(
            settings.WS_URL+f"?secret={settings.WS_SECRET}", namespaces=["/jobs"])
        # Intercepting the logs to add data into the log-file and sending them
        # to a websocket
        log_file = io.StringIO()
        logger.add(log_file)
        logger.add(InterceptionHandler(job_id=job_id, socket=sio))

        # Incrementing and getting the current number of used rfb ports
        # (+1 for this new task)
        current_used_rfb_ports = task_utils.incr_used_rfb_ports()

        try:
            content = bot_utils.download_bot(s3_path).decode()
            print(f"RUNNING: {bot_id}; [{job_id}]")

            if settings.SELENIUM_DRIVER_INITIALIZER is not None:
                mod_name, func_name = settings.SELENIUM_DRIVER_INITIALIZER.rsplit('.', 1)
                package = importlib.import_module(mod_name)
                get_driver = getattr(package, func_name)

            with Display(
                backend='xvnc',
                size=(1920, 1080),
                # File containing the vnc password, generated with `vncpasswd`
                rfbauth="/code/xvnc_passwd",
                manage_global_env=False,
                rfbport=5900+current_used_rfb_ports,
            ) as display:
                # TODO: Set up tracking to track which bot is running at which port
                # Creating a VNC Server at :rfb_port and forwarding it over a
                # Websockify Proxy at :websockify_port which can be connected to
                # via noVNC
                display_num = display.display
                rfb_port = display._obj._rfbport
                logger.debug(f"Running VNC for :{display_num} at [{rfb_port}].")
                assert rfb_port < 5999
                websockify_port = rfb_port - 100
                logger.debug(f"Running websockify for :{display_num} at [{websockify_port}]")
                # TODO: Switch to wss using a proper cert/key
                # TODO 1: Add CORS Headers
                # Add `ssl_only`, `verify_client`, and `cafile`
                websockify_proc = Process(
                    target=run_websockify,
                    args=(websockify_port, rfb_port)
                )
                websockify_proc.start()
                # Waiting for the websockify port to be available
                if task_utils.wait_for_port(websockify_port):
                    job.vnc_ws_proxy_port = websockify_port
                    db.session.commit()
                else:
                    raise ValueError(f"Unable to connect to websockify port for {job_id}")

                with task_utils.with_env(display.env()):
                    try:
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
                    finally:
                        websockify_proc.terminate()
                        websockify_proc.join()

            emit_job_message(
                sio,
                {
                    "id": job_id,
                    "log": "-- Finished --",
                    "finish_time": datetime.now().isoformat()
                })
        finally:
            # Decrementing the used-rfb-ports
            task_utils.decr_used_rfb_ports()
            # Marking the job as finished + setting logs in the db
            job.finish_time = datetime.now()
            log_file.seek(0)
            job.logs = log_file.getvalue()
            db.session.commit()
            sio.disconnect()
