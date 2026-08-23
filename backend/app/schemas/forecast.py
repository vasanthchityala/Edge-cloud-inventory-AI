from datetime import date

from pydantic import BaseModel


class ForecastResponse(BaseModel):
    id: int
    store_id: int
    product_id: int
    forecast_date: date
    predicted_demand: float
    model_version: str

    class Config:
        from_attributes = True 