from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.models.product import Product
from backend.app.schemas.product import ProductCreate
from backend.app.services.product_service import get_all_products


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    new_product = Product(
        sku=product.sku,
        name=product.name,
        category=product.category,
        unit_price=product.unit_price,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product