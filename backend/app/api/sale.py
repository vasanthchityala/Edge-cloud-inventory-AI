from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.models.sale import Sale
from backend.app.schemas.sale import SaleCreate
from backend.app.services.sale_service import get_all_sales


router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_sales(db: Session = Depends(get_db)):
    return get_all_sales(db)


@router.post("/")
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
):
    new_sale = Sale(
        store_id=sale.store_id,
        product_id=sale.product_id,
        sale_date=sale.sale_date,
        quantity=sale.quantity,
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale