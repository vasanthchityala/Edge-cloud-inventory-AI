from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.schemas.validated_action import (
    ValidatedActionResponse,
)
from backend.app.services.validated_action_service import (
    get_validated_actions,
)


router = APIRouter(
    prefix="/validated-actions",
    tags=["Validated Actions"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[ValidatedActionResponse],
)
def get_actions(
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

    validation_status: str | None = Query(
        default=None,
    ),

    priority: str | None = Query(
        default=None,
    ),

    db: Session = Depends(get_db),
):

    return get_validated_actions(
        db=db,
        skip=skip,
        limit=limit,
        store_id=store_id,
        product_id=product_id,
        validation_status=validation_status,
        priority=priority,
    )