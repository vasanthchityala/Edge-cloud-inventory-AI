from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.inventory import Inventory


def get_all_inventory(db: Session) -> list[Inventory]:
    result = db.execute(select(Inventory))
    return list(result.scalars().all())