from .base import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = "<SECRET_KEY>"
