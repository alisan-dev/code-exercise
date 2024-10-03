from __future__ import annotations

from pydantic import BaseModel, Field, conlist, model_validator

__all__ = (
    "PredictionRequestData",
    "PredictionResponse",
    "PredictionResponseProbabilityData",
)


class PredictionRequestData(BaseModel):
    Material_A_Charged_Amount: list[conlist(item_type=float, min_length=1, max_length=1)] = Field(default=[], min_length=1)  # type: ignore # noqa: E501
    Material_B_Charged_Amount: list[conlist(item_type=float, min_length=1, max_length=1)] = Field(default=[], min_length=1)  # type: ignore # noqa: E501
    Reactor_Volume: list[conlist(item_type=float, min_length=1, max_length=1)] = Field(default=[], min_length=1)  # type: ignore # noqa: E501
    Material_A_Final_Concentration_Previous_Batch: list[conlist(item_type=float, min_length=1, max_length=1)] = Field(default=[], min_length=1)  # type: ignore # noqa: E501

    @model_validator(mode="after")  # type: ignore[arg-type]
    @classmethod
    def validate_values(cls, values: PredictionRequestData) -> PredictionRequestData:  # noqa: N805
        length_of_values = [len(list_of_values) for list_of_values in values.model_dump().values()]
        if not all(length_of_values):
            raise ValueError("The data for all inputs should be provided correctly.")
        elif len(set(length_of_values)) > 1:
            raise ValueError("All values must have same number of items.")
        return values


class PredictionResponseProbabilityData(BaseModel):
    Good: float
    High: float
    Low: float


class PredictionResponse(BaseModel):
    output_label: str
    output_probability: PredictionResponseProbabilityData
