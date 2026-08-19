from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database.base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

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

    current_stock: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    safety_stock: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    capacity: Mapped[int] = mapped_column(
        nullable=False,
    )