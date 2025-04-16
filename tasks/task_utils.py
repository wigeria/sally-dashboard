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


def lock_new_rfb_port():
    """ Adds the smallest unused RFB port to the list of used_rfb_ports.

        This function searches for the smallest port number in the range
        from 5800 to 5899 that is not currently in use and adds it to the
        list of used RFB ports in Redis. If a port is successfully
        allocated, it returns the port number. If no ports are available,
        it returns -1.
        Returns:
            int: The newly allocated RFB port number if successful;
            -1 if all ports in the specified range are currently in use.
    """
    r = redis.Redis(host=settings.REDIS_CONF['host'],
                    port=settings.REDIS_CONF['port'],
                    db=settings.REDIS_CONF['db'])
    key = 'sally:vnc:used_rfb_ports'
    available_ports = list(range(5900, 6000))  # List of ports from 5800 to 5899

    with redis_lock(r, key, 10):
        used_ports = r.lrange(key, 0, -1)
        used_ports = [int(port) for port in used_ports]  # Convert bytes to integers

        # Find the smallest unused port
        for port in available_ports:
            if port not in used_ports:
                r.rpush(key, port)
                return port

    raise ValueError("No available port")


def unlock_rfb_port(port):
    """ Decrements the used_rfb_ports value by removing the specified port

        Returns:
            bool: True if the port was successfully removed, False otherwise
    """
    r = redis.Redis(host=settings.REDIS_CONF['host'],
                    port=settings.REDIS_CONF['port'],
                    db=settings.REDIS_CONF['db'])
    key = 'sally:vnc:used_rfb_ports'

    with redis_lock(r, key, 10):
        used_ports = r.lrange(key, 0, -1)
        used_ports = [int(p) for p in used_ports]  # Convert bytes to integers

        if port in used_ports:
            r.lrem(key, 1, port)  # Remove the specified port
            return True

    return False  # Indicate that the port was not found


def clear_used_rfb_ports():
    """ Clears all of the used RFB ports from Redis """
    r = redis.Redis(host=settings.REDIS_CONF['host'],
                    port=settings.REDIS_CONF['port'],
                    db=settings.REDIS_CONF['db'])
    key = 'sally:vnc:used_rfb_ports'

    with redis_lock(r, key, 10):
        r.delete(key)  # Clear the list of used RFB ports


@contextmanager
def with_env(custom_env: dict):
    """ Async context manager for custom environment """
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
