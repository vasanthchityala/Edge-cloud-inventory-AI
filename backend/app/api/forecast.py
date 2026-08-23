from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.database.session import SessionLocal
from backend.app.schemas.forecast import ForecastResponse
from backend.app.services.forecast_service import get_forecasts


router = APIRouter(
    prefix="/forecasts",
    tags=["Forecasts"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/",
    response_model=list[ForecastResponse],
)
def get_forecast_data(
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

    forecast_date: date | None = Query(
        default=None,
    ),

    db: Session = Depends(get_db),
):

    return get_forecasts(
        db=db,
        skip=skip,
        limit=limit,
        store_id=store_id,
        product_id=product_id,
        forecast_date=forecast_date,
    )