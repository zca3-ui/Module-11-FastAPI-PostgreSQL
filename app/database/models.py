
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    CheckConstraint,
)
from sqlalchemy.sql import func

from app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=True
    )


class Calculation(Base):
    __tablename__ = "calculations"

    __table_args__ = (
        CheckConstraint(
            "type IN ('Add', 'Sub', 'Multiply', 'Divide')",
            name="check_calculation_type"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    a = Column(Float, nullable=False)

    b = Column(Float, nullable=False)

    type = Column(String(10), nullable=False)
