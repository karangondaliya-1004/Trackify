import os

from dotenv import load_dotenv

load_dotenv()

from .development import DevelopmentConfig  # noqa: E402
from .production import ProductionConfig  # noqa: E402

ENV = os.getenv("ENV", "development")

config = DevelopmentConfig() if ENV == "development" else ProductionConfig()
