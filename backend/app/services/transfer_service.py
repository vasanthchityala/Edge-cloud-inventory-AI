from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.transfer import Transfer


def get_all_transfers(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    from_store_id: int | None = None,
    to_store_id: int | None = None,
    product_id: int | None = None,
) -> list[Transfer]:

    query = select(Transfer)

    if from_store_id is not None:
        query = query.where(
            Transfer.from_store_id == from_store_id
        )

    if to_store_id is not None:
        query = query.where(
            Transfer.to_store_id == to_store_id
        )

    if product_id is not None:
        query = query.where(
            Transfer.product_id == product_id
        )

    query = (
        query
        .order_by(Transfer.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = db.execute(query)

    return list(result.scalars().all())


def create_transfer(
    db: Session,
    from_store_id: int,
    to_store_id: int,
    product_id: int,
    quantity: int,
    status: str = "recommended",
) -> Transfer:

    transfer = Transfer(
        from_store_id=from_store_id,
        to_store_id=to_store_id,
        product_id=product_id,
        quantity=quantity,
        status=status,
        created_at=datetime.utcnow(),
    )

    db.add(transfer)
    db.commit()
    db.refresh(transfer)

    return transfer