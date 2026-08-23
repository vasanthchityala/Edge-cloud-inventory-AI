from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.forecast import Forecast


def get_forecasts(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    store_id: int | None = None,
    product_id: int | None = None,
    forecast_date: date | None = None,
) -> list[Forecast]:

    query = select(Forecast)

    if store_id is not None:
        query = query.where(
            Forecast.store_id == store_id
        )

    if product_id is not None:
        query = query.where(
            Forecast.product_id == product_id
        )

    if forecast_date is not None:
        query = query.where(
            Forecast.forecast_date == forecast_date
        )

    query = (
        query
        .order_by(Forecast.forecast_date)
        .offset(skip)
        .limit(limit)
    )

    result = db.execute(query)

    return list(result.scalars().all())