from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base


class UnifiedPriority(Base):
    __tablename__ = "unified_priority"

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

    category: Mapped[str] = mapped_column(
        String(100),
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

    forecast_demand: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    edge_low_stock_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    from_store_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    priority_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    unified_priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )