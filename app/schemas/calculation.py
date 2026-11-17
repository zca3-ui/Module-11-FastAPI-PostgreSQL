
import math
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CalculationType(str, Enum):
    ADD = "Add"
    SUB = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationCreate(BaseModel):
    a: float = Field(..., allow_inf_nan=False)
    b: float = Field(..., allow_inf_nan=False)
    type: CalculationType

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_division(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Cannot divide by zero.")

        return self


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: float

    model_config = ConfigDict(from_attributes=True)
