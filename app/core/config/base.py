class BaseConfig:
    APP_NAME = "Multi-Tenant Subscription Billing & Usage Platform"
    DEBUG = False
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
