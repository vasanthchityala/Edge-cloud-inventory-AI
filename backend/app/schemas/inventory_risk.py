from datetime import date

from pydantic import BaseModel


class InventoryRiskResponse(BaseModel):
    id: int
    date: date

    store_id: int
    product_id: int
    category: str

    target_demand: float
    predicted_demand: float
    forecast_error: float
    absolute_error: float

    current_stock: int
    safety_stock: int
    capacity: int
    lead_time_days: int

    forecast_demand: float
    projected_stock: float
    required_stock: float
    stock_surplus: float

    risk_level: str

    class Config:
        from_attributes = True