import os
from .development import DevelopmentConfig
from .production import ProductionConfig

ENV = os.getenv("ENV","development")

config = DevelopmentConfig() if ENV=="development" else ProductionConfig() 