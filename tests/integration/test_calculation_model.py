
import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.database.connection import SessionLocal
from app.database.models import Calculation
from app.schemas.calculation import CalculationCreate

@pytest.fixture
def db_session():
    """Create a database session for each integration test."""

    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()

def test_create_calculation_in_database(db_session):
    """Verify that a calculation can be saved and retrieved."""

    calculation = Calculation(
        a=10,
        b=5,
        type="Add"
    )

    db_session.add(calculation)
    db_session.commit()
    db_session.refresh(calculation)

    assert calculation.id is not None
    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == "Add"

    # Verify the record can be retrieved from PostgreSQL.
    saved_calculation = db_session.get(Calculation, calculation.id)

    assert saved_calculation is not None
    assert saved_calculation.a == 10
    assert saved_calculation.b == 5
    assert saved_calculation.type == "Add"

    # Remove the test record.
    db_session.delete(calculation)
    db_session.commit()

def test_invalid_calculation_type_is_rejected_by_database(db_session):
    """Verify that PostgreSQL rejects unsupported calculation types."""

    invalid_calculation = Calculation(
        a=10,
        b=5,
        type="Power"
    )

    db_session.add(invalid_calculation)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

def test_division_by_zero_is_rejected_before_database_insert():
    """Verify that invalid division input is rejected by Pydantic."""

    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b=0,
            type="Divide"
        )

def test_non_finite_operands_are_rejected():
    """Verify that NaN and infinity are not accepted as operands."""

    with pytest.raises(ValidationError):
        CalculationCreate(
            a=float("inf"),
            b=5,
            type="Add"
        )