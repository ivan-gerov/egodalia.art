from __future__ import annotations

import os
from portfolio.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", ".vercel.app", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("PORTFOLIO_DB_NAME"),
        "USER": os.getenv("PORTFOLIO_DB_USER"),
        "PASSWORD": os.getenv("PORTFOLIO_DB_PWD"),
        "HOST": os.getenv("PORTFOLIO_DB_HOST"),
        "PORT": os.getenv("PORTFOLIO_DB_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}


DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

WSGI_APPLICATION = "vercel_app.wsgi.app"


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles_build" / "static"

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",
    "http://parfume-fe.vercel.app",
]
