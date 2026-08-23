from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base


class ValidatedAction(Base):
    __tablename__ = "validated_actions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    store_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    from_store_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    current_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    safety_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    forecast_demand: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    validation_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    validation_reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    required_stock: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stock_after_transfer: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    remaining_shortage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )