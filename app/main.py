import logging
import os

from fastapi import FastAPI

from app.health import router as health_router

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("fastapi-devops-cicd")

app = FastAPI(
    title="FastAPI DevOps CI/CD Demo",
    version=APP_VERSION,
)
app.include_router(health_router)


@app.get("/")
def root() -> dict[str, str]:
    logger.info("Root endpoint called")
    return {"message": "FastAPI DevOps CI/CD demo"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": APP_VERSION}

