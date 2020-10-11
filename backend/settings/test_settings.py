""" Contains test settings used when os.environ['TEST'] == 'True' """

import os


DATABASE_URI = os.environ["TEST_DATABASE_URI"]
REDIS_CONF = {
    "host": os.environ.get("TEST_REDIS_HOST", None),
    "port": os.environ.get("TEST_REDIS_PORT", 6379),
    "db": 0
}
