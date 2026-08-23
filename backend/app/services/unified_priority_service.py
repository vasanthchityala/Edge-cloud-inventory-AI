from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.unified_priority import UnifiedPriority


def get_unified_priorities(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    store_id: int | None = None,
    product_id: int | None = None,
    risk_level: str | None = None,
    unified_priority: str | None = None,
) -> list[UnifiedPriority]:

    query = select(UnifiedPriority)

    if store_id is not None:
        query = query.where(
            UnifiedPriority.store_id == store_id
        )

    if product_id is not None:
        query = query.where(
            UnifiedPriority.product_id == product_id
        )

    if risk_level is not None:
        query = query.where(
            UnifiedPriority.risk_level == risk_level.upper()
        )

    if unified_priority is not None:
        query = query.where(
            UnifiedPriority.unified_priority
            == unified_priority.upper()
        )

    query = (
        query
        .order_by(
            UnifiedPriority.priority_score.desc()
        )
        .offset(skip)
        .limit(limit)
    )

    result = db.execute(query)

    return list(
        result.scalars().all()
    )