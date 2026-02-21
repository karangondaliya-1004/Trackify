import os

from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = "<SECRET_KEY>"
