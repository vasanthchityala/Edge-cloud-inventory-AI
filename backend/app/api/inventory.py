from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.models.inventory import Inventory
from backend.app.schemas.inventory import InventoryCreate
from backend.app.services.inventory_service import get_all_inventory


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_inventory(db: Session = Depends(get_db)):
    return get_all_inventory(db)


@router.post("/")
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db),
):
    new_inventory = Inventory(
        store_id=inventory.store_id,
        product_id=inventory.product_id,
        current_stock=inventory.current_stock,
        safety_stock=inventory.safety_stock,
        capacity=inventory.capacity,
    )

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory