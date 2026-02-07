from fastapi import FastAPI
from app.core.config import config


app = FastAPI(title=config.APP_NAME,debug=getattr(config, "DEBUG", False))

@app.get("/health",tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "environment": config.__class__.__name__,
        "service": "saas-core",
        "message": "Service is running"
    }