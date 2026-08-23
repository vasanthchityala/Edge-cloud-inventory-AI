from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base


class InventoryRisk(Base):
    __tablename__ = "inventory_risk"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target_demand: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    predicted_demand: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    forecast_error: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    absolute_error: Mapped[float] = mapped_column(
        Float,
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

    lead_time_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    forecast_demand: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    projected_stock: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    required_stock: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    stock_surplus: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )