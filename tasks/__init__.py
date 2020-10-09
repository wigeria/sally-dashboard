""" Package containing the dramatiq tasks (actors)
    Run workers using `flask worker --processes=1`
"""

from backend import settings
import dramatiq
from dramatiq.brokers.redis import RedisBroker
import os


if os.environ.get("TEST", "False") == "True":
    broker = RedisBroker(**settings.TEST_REDIS_CONF)
else:
    broker = RedisBroker(**settings.REDIS_CONF)
dramatiq.set_broker(broker)

