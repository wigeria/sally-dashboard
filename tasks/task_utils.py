from flask import Flask
from backend.database import db
from backend.database.models import Job
from . import settings
import time
import socket
from unittest.mock import patch
from contextlib import contextmanager
import redis  # type: ignore


class TaskContextManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URI
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)

    def __enter__(self):
        self.ctx = self.app.app_context()
        self.ctx.push()
        return db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx.pop()


@contextmanager
def redis_lock(redis_client, key: str, timeout: int = 10):
    """Context manager for Redis lock."""
    lock_key = f"{key}:lock"
    lock = redis_client.lock(lock_key, timeout=timeout)
    try:
        lock.acquire()
        yield
    finally:
        lock.release()


# TODO: Change the redis logic to be a list of used-ports, and remove ports on
# task finish. Take the smallest port between 5800-5899 that is unused.
def incr_used_rfb_ports():
    """ Increments the used_rfb_ports value by 1

        Returns:
            int: The incremented used_rfb_ports value
    """
    r = redis.Redis(host=settings.REDIS_CONF['host'],
                    port=settings.REDIS_CONF['port'],
                    db=settings.REDIS_CONF['db'])
    key = 'sally:vnc:used_rfb_ports'
    with redis_lock(r, key, 10):
        value = r.get(key)
        # Returns 1 if there aren't any used-rfb-ports
        if value is None:
            r.set(key, 1)
            return 1
        else:
            # Otherwise, increments it
            new_value = int(value) + 1
            r.set(key, new_value)
            return new_value


def decr_used_rfb_ports():
    """ Decrements the used_rfb_ports value by 1"""
    r = redis.Redis(host=settings.REDIS_CONF['host'],
                    port=settings.REDIS_CONF['port'],
                    db=settings.REDIS_CONF['db'])
    key = 'sally:vnc:used_rfb_ports'
    with redis_lock(r, key, 60):
        value = r.get(key)
        if value is not None and value != 0:
            new_value = max(1, int(value) - 1)
            r.set(key, new_value)
            return new_value
        return 0


@contextmanager
def with_env(custom_env: dict):
    """Async context manager for custom environment"""
    with patch.dict('os.environ', custom_env, clear=True):
        yield


def wait_for_port(port, timeout=10):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return True
        except (ConnectionRefusedError, socket.timeout):
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.5)
