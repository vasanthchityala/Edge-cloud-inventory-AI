from pydantic import BaseModel


class ValidatedActionResponse(BaseModel):
    id: int

    store_id: int
    product_id: int

    action: str
    quantity: int
    from_store_id: int | None

    priority: str
    reason: str

    current_stock: int
    safety_stock: int
    capacity: int
    forecast_demand: float

    validation_status: str
    validation_reason: str

    required_stock: float
    stock_after_transfer: float
    remaining_shortage: float

    class Config:
        from_attributes = True