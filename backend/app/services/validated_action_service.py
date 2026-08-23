from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.validated_action import ValidatedAction


def get_validated_actions(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    store_id: int | None = None,
    product_id: int | None = None,
    validation_status: str | None = None,
    priority: str | None = None,
) -> list[ValidatedAction]:

    query = select(ValidatedAction)

    if store_id is not None:
        query = query.where(
            ValidatedAction.store_id == store_id
        )

    if product_id is not None:
        query = query.where(
            ValidatedAction.product_id == product_id
        )

    if validation_status is not None:
        query = query.where(
            ValidatedAction.validation_status
            == validation_status.upper()
        )

    if priority is not None:
        query = query.where(
            ValidatedAction.priority
            == priority.upper()
        )

    query = (
        query
        .order_by(
            ValidatedAction.id
        )
        .offset(skip)
        .limit(limit)
    )

    result = db.execute(query)

    return list(
        result.scalars().all()
    )