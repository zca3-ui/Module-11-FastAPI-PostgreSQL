
import pytest
from pydantic import ValidationError

from app.operations.factory import CalculationFactory
from app.schemas.calculation import CalculationCreate, CalculationType


@pytest.mark.parametrize(
    "a, b, operation, expected",
    [
        (10, 5, CalculationType.ADD, 15),
        (10, 5, CalculationType.SUB, 5),
        (10, 5, CalculationType.MULTIPLY, 50),
        (10, 5, CalculationType.DIVIDE, 2),
    ],
)
def test_calculation_factory(a, b, operation, expected):
    result = CalculationFactory.calculate(a, b, operation)
    assert result == expected


def test_division_by_zero():
    with pytest.raises(ValueError):
        CalculationFactory.calculate(10, 0, CalculationType.DIVIDE)


def test_invalid_operation():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="Power")


def test_schema_rejects_division_by_zero():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=0, type="Divide")


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_schema_rejects_non_finite_numbers(value):
    with pytest.raises(ValidationError):
        CalculationCreate(a=value, b=5, type="Add")


def test_schema_rejects_unexpected_fields():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="Add", username="testuser")

def test_factory_rejects_unsupported_operation():
    with pytest.raises(ValueError):
        CalculationFactory.calculate(10, 5, "Power")