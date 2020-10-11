""" Package containing the dramatiq tasks (actors)
    Run workers using `flask worker --processes=1`
"""

from backend import settings
import dramatiq
from dramatiq.brokers.redis import RedisBroker
import os


broker = RedisBroker(**settings.REDIS_CONF)
dramatiq.set_broker(broker)
