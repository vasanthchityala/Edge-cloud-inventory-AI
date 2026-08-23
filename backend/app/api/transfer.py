from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.schemas.transfer import (
    TransferCreate,
    TransferResponse,
)
from backend.app.services.transfer_service import (
    create_transfer,
    get_all_transfers,
)


router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[TransferResponse],
)
def get_transfers(
    skip: int = Query(
        default=0,
        ge=0,
    ),

    limit: int = Query(
        default=50,
        ge=1,
        le=500,
    ),

    from_store_id: int | None = Query(
        default=None,
    ),

    to_store_id: int | None = Query(
        default=None,
    ),

    product_id: int | None = Query(
        default=None,
    ),

    db: Session = Depends(get_db),
):

    return get_all_transfers(
        db=db,
        skip=skip,
        limit=limit,
        from_store_id=from_store_id,
        to_store_id=to_store_id,
        product_id=product_id,
    )


@router.post(
    "/",
    response_model=TransferResponse,
)
def add_transfer(
    transfer: TransferCreate,
    db: Session = Depends(get_db),
):

    return create_transfer(
        db=db,
        from_store_id=transfer.from_store_id,
        to_store_id=transfer.to_store_id,
        product_id=transfer.product_id,
        quantity=transfer.quantity,
        status=transfer.status,
    )