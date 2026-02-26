import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger.json import JsonFormatter

from app.config import settings
from app.health import router as health_router

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
logging.basicConfig(level=settings.log_level.upper(), handlers=[handler])
logger = logging.getLogger("fastapi-devops-cicd")

app = FastAPI(
    title="FastAPI DevOps CI/CD Demo",
    version=settings.app_version,
)
app.include_router(health_router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def root() -> dict[str, str]:
    logger.info("Root endpoint called")
    return {"message": "FastAPI DevOps CI/CD demo"}


@app.get("/version")
def version() -> dict[str, str]:
    return {"version": settings.app_version}
