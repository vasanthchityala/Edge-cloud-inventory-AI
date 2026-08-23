from pydantic import BaseModel


class UnifiedPriorityResponse(BaseModel):
    id: int

    store_id: int
    product_id: int
    category: str

    current_stock: int
    safety_stock: int
    forecast_demand: float

    risk_level: str
    edge_low_stock_count: int

    action: str
    quantity: float
    from_store_id: int | None

    priority_score: float
    unified_priority: str

    class Config:
        from_attributes = True