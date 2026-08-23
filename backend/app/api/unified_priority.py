from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.schemas.unified_priority import (
    UnifiedPriorityResponse,
)
from backend.app.services.unified_priority_service import (
    get_unified_priorities,
)


router = APIRouter(
    prefix="/unified-priority",
    tags=["Unified Priority"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[UnifiedPriorityResponse],
)
def get_priority_data(
    skip: int = Query(
        default=0,
        ge=0,
    ),

    limit: int = Query(
        default=50,
        ge=1,
        le=500,
    ),

    store_id: int | None = Query(
        default=None,
    ),

    product_id: int | None = Query(
        default=None,
    ),

    risk_level: str | None = Query(
        default=None,
    ),

    unified_priority: str | None = Query(
        default=None,
    ),

    db: Session = Depends(get_db),
):

    return get_unified_priorities(
        db=db,
        skip=skip,
        limit=limit,
        store_id=store_id,
        product_id=product_id,
        risk_level=risk_level,
        unified_priority=unified_priority,
    )