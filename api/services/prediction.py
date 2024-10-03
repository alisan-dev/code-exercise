from __future__ import annotations

import logging

import numpy
from onnxruntime import InferenceSession

from api.models.prediction import PredictionResponse

__all__ = (
    "PredictionService",
)

logger = logging.getLogger(__name__)


class PredictionService:
    @staticmethod
    def prepare_input_feed(data: dict) -> dict:
        input_feed: dict = {}
        for field, values in data.items():
            input_feed[field] = numpy.array(values).reshape(len(values), 1).astype(numpy.float32)

        return input_feed

    @classmethod
    def predict(cls, data: dict) -> list[PredictionResponse]:
        input_feed: dict = cls.prepare_input_feed(data)
        session = InferenceSession("fixtures/ml_models/model.onnx", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])  # noqa: E501
        labels, probabilities = session.run([], input_feed)

        logger.info(f"The model computed predictions with -> {labels=} {probabilities=}.")

        response: list[PredictionResponse] = []
        for index in range(len(labels)):
            response.append(
                PredictionResponse(
                    output_label=labels[index],
                    output_probability=probabilities[index]
                )
            )
        return response
