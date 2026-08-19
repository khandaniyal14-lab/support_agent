from fastapi import FastAPI

from app.api.routes.agents import (
    router as agent_router,
)
from app.api.routes.ai import router as ai_router
from app.api.routes.health import router as health_router
from app.api.routes.rag import router as rag_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.3.0",
    debug=settings.debug,
)


app.include_router(
    health_router
)

app.include_router(
    ai_router
)

app.include_router(
    rag_router
)

app.include_router(
    agent_router
)


@app.get("/")
def root():
    return {
        "application": settings.app_name,
        "version": "0.3.0",
        "status": "running",
    }