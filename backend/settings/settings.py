""" Settings used when not in TEST mode """

import os


DATABASE_URI = os.environ["DATABASE_URI"]
REDIS_CONF = {
    "host": os.environ.get("REDIS_HOST", None),
    "port": os.environ.get("REDIS_PORT", 6379),
    "db": 0
}
