from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.schemas.inventory_risk import (
    InventoryRiskResponse,
)
from backend.app.services.inventory_risk_service import (
    get_inventory_risks,
)


router = APIRouter(
    prefix="/inventory-risk",
    tags=["Inventory Risk"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[InventoryRiskResponse],
)
def get_inventory_risk_data(
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

    db: Session = Depends(get_db),
):

    return get_inventory_risks(
        db=db,
        skip=skip,
        limit=limit,
        store_id=store_id,
        product_id=product_id,
        risk_level=risk_level,
    )