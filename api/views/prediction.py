import logging

from fastapi import APIRouter, Security
from fastapi.security import APIKeyHeader

from api.models.prediction import PredictionRequestData, PredictionResponse
from api.services.prediction import PredictionService

__all__ = (
    "prediction_router",
)

logger = logging.getLogger(__name__)

prediction_router = APIRouter(
    tags=["CODE EXERCISE PREDICTION"],
    dependencies=[Security(APIKeyHeader(name="apikey"))],
    responses={
        400: {"description": "Missing/Invalid request_data or query_params."},
        500: {"description": "An unexpected error has occurred"},
    }
)


@prediction_router.post(
    "/predict",
    response_model=list[PredictionResponse],
    summary="Code Exercise Prediction API",
    description="Code Exercise Prediction API",
    operation_id="code_exercise_prediction-api",
)
async def prediction_api(request_data: PredictionRequestData) -> list[PredictionResponse]:
    logger.info(f"Prediction API is called -> {request_data=}")

    return PredictionService.predict(request_data.model_dump())
