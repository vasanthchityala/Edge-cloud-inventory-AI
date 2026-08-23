from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.inventory_risk import InventoryRisk


def get_inventory_risks(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    store_id: int | None = None,
    product_id: int | None = None,
    risk_level: str | None = None,
) -> list[InventoryRisk]:

    query = select(InventoryRisk)

    if store_id is not None:
        query = query.where(
            InventoryRisk.store_id == store_id
        )

    if product_id is not None:
        query = query.where(
            InventoryRisk.product_id == product_id
        )

    if risk_level is not None:
        query = query.where(
            InventoryRisk.risk_level == risk_level.upper()
        )

    query = (
        query
        .order_by(InventoryRisk.id)
        .offset(skip)
        .limit(limit)
    )

    result = db.execute(query)

    return list(
        result.scalars().all()
    )