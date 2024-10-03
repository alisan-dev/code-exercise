import logging

from fastapi import FastAPI

__all__ = (
    "app",
)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    from api.views.prediction import prediction_router

    _app = FastAPI(
        title="API Documentation",
        version="0.1.0",
    )
    _app.include_router(prediction_router)

    return _app


app = create_app()
