
from app.operations import add, subtract, multiply, divide
from app.schemas.calculation import CalculationType


class CalculationFactory:
    """Selects and executes the requested calculation operation."""

    _operations = {
        CalculationType.ADD: add,
        CalculationType.SUB: subtract,
        CalculationType.MULTIPLY: multiply,
        CalculationType.DIVIDE: divide,
    }

    @classmethod
    def calculate(cls, a: float, b: float, operation: CalculationType) -> float:
        """Execute the selected calculation."""

        try:
            calculation = cls._operations[operation]
        except KeyError:
            raise ValueError(f"Unsupported calculation type: {operation}")

        return float(calculation(a, b))
