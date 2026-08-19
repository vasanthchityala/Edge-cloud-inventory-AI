from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.product import Product


def get_all_products(db: Session) -> list[Product]:
    result = db.execute(select(Product))
    return list(result.scalars().all())