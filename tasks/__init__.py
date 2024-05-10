""" Package containing the dramatiq tasks (actors)
    Run workers using `flask worker --processes=1`
"""

from backend import settings
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.rate_limits.backends import RedisBackend
import os


broker = RedisBroker(**settings.REDIS_CONF)
dramatiq.set_broker(broker)

backend = RedisBackend(**settings.REDIS_CONF)
# Hard coded to 4 concurrent tasks at a time
DISTRIBUTED_MUTEX = ConcurrentRateLimiter(
    backend, "distributed-mutex", limit=4)
