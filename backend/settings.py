""" Contains configuration details for the backend """

import os
import sys


PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
MIGRATIONS_DIR = os.path.join(PROJECT_DIR, "migrations")

# Deployment Settings
DEBUG = os.environ.get("DEBUG", "False") == "True"
HOST = os.environ.get("HOST", "localhost")
PORT = sys.argv[-1] if sys.argv[-1].isdigit() else \
    os.environ.get("PORT", "8080")

# Database Settings
TEST_DATABASE_URI = os.environ["TEST_DATABASE_URI"]
DATABASE_URI = os.environ["DATABASE_URI"]

# Auth Settings
SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
JWT_TIMEOUT = 3600

# AWS Settings
AWS_ACCESS = os.environ.get("AWS_ACCESS", None)
AWS_SECRET = os.environ.get("AWS_SECRET", None)
AWS_BUCKET = os.environ.get("AWS_BUCKET", None)

# Redis Settings
REDIS_CONF = {
    "host": os.environ.get("REDIS_HOST", None),
    "port": os.environ.get("REDIS_PORT", 6379),
    "db": 0
}
TEST_REDIS_CONF = {
    "host": os.environ.get("TEST_REDIS_HOST", None),
    "port": os.environ.get("TEST_REDIS_PORT", 6379),
    "db": 0
}
