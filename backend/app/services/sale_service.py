from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.sale import Sale


def get_all_sales(db: Session) -> list[Sale]:
    result = db.execute(select(Sale))
    return list(result.scalars().all())