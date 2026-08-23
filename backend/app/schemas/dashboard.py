from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_stores: int
    total_products: int

    total_inventory_records: int
    total_forecast_records: int

    total_inventory_risk_records: int
    high_risk_items: int
    critical_priority_items: int

    total_transfers: int
    total_validated_actions: int

    valid_actions: int
    partial_actions: int

    total_remaining_shortage: float