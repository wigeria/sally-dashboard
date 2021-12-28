import os
import sys


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MIGRATIONS_DIR = os.path.join(PROJECT_DIR, "migrations")

# Deployment Settings
DEBUG = os.environ.get("DEBUG", "False") == "True"
HOST = os.environ.get("HOST", "localhost")
PORT = sys.argv[-1] if sys.argv[-1].isdigit() else \
    os.environ.get("PORT", "5000")

# Auth Settings
SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")
JWT_TIMEOUT = 3600

# AWS Settings
AWS_ACCESS = os.environ.get("AWS_ACCESS", None)
AWS_SECRET = os.environ.get("AWS_SECRET", None)
AWS_BUCKET = os.environ.get("AWS_BUCKET", None)

WS_URL = f"http://{HOST}:{PORT}"
WS_SECRET = os.environ.get("WS_SECRET", None)

if os.environ.get("TEST", "False") == "True":
    from .test_settings import *
else:
    from .settings import *

# Setting that must point to a callable that returns a selenium webdriver
# implementor (ex "plugins.custom_plugin.module.initializer") if set
SELENIUM_DRIVER_INITIALIZER = os.environ.get(
    "SELENIUM_DRIVER_INITIALIZER", None)
