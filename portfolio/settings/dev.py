from __future__ import annotations
import os

from dotenv import load_dotenv

load_dotenv()

from portfolio.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

USE_PRODUCTION_DB = bool(os.getenv("DEV_USE_PROD_DB", False))


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

if USE_PRODUCTION_DB:
    from portfolio.settings.prod import DATABASES

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
