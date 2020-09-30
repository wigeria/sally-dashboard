""" Contains configuration details for the backend """

import os
import sys


# Deployment Settings
DEBUG = os.environ.get("DEBUG", "False") == "True"
HOST = os.environ.get("HOST", "localhost")
PORT = sys.argv[-1] if sys.argv[-1].isdigit() else \
    os.environ.get("PORT", "8080")

# Database Settings
TEST_DATABASE_URI = os.environ["TEST_DATABASE_URI"]
DATABASE_URI = os.environ["DATABASE_URI"]