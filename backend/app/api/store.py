from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.models.store import Store
from backend.app.schemas.store import StoreCreate
from backend.app.services.store_service import get_all_stores


router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_stores(db: Session = Depends(get_db)):
    return get_all_stores(db)


@router.post("/")
def create_store(
    store: StoreCreate,
    db: Session = Depends(get_db),
):
    new_store = Store(
        name=store.name,
        location=store.location,
    )

    db.add(new_store)
    db.commit()
    db.refresh(new_store)

    return new_store