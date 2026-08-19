from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.store import Store


def get_all_stores(db: Session) -> list[Store]:
    result = db.execute(select(Store))
    return list(result.scalars().all())