from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.store import Store
from backend.app.models.product import Product
from backend.app.models.inventory import Inventory
from backend.app.models.forecast import Forecast
from backend.app.models.inventory_risk import InventoryRisk
from backend.app.models.transfer import Transfer
from backend.app.models.unified_priority import UnifiedPriority
from backend.app.models.validated_action import ValidatedAction


def get_dashboard_summary(db: Session):

    total_stores = db.scalar(
        select(func.count(Store.id))
    ) or 0

    total_products = db.scalar(
        select(func.count(Product.id))
    ) or 0

    total_inventory_records = db.scalar(
        select(func.count(Inventory.id))
    ) or 0

    total_forecast_records = db.scalar(
        select(func.count(Forecast.id))
    ) or 0

    total_inventory_risk_records = db.scalar(
        select(func.count(InventoryRisk.id))
    ) or 0

    high_risk_items = db.scalar(
        select(func.count(InventoryRisk.id))
        .where(
            InventoryRisk.risk_level == "HIGH"
        )
    ) or 0

    critical_priority_items = db.scalar(
        select(func.count(UnifiedPriority.id))
        .where(
            UnifiedPriority.unified_priority == "CRITICAL"
        )
    ) or 0

    total_transfers = db.scalar(
        select(func.count(Transfer.id))
    ) or 0

    total_validated_actions = db.scalar(
        select(func.count(ValidatedAction.id))
    ) or 0

    valid_actions = db.scalar(
        select(func.count(ValidatedAction.id))
        .where(
            ValidatedAction.validation_status == "VALID"
        )
    ) or 0

    partial_actions = db.scalar(
        select(func.count(ValidatedAction.id))
        .where(
            ValidatedAction.validation_status == "PARTIAL"
        )
    ) or 0

    total_remaining_shortage = db.scalar(
        select(
            func.coalesce(
                func.sum(
                    ValidatedAction.remaining_shortage
                ),
                0,
            )
        )
    ) or 0

    return {
        "total_stores": total_stores,
        "total_products": total_products,
        "total_inventory_records": total_inventory_records,
        "total_forecast_records": total_forecast_records,
        "total_inventory_risk_records":
            total_inventory_risk_records,
        "high_risk_items": high_risk_items,
        "critical_priority_items":
            critical_priority_items,
        "total_transfers": total_transfers,
        "total_validated_actions":
            total_validated_actions,
        "valid_actions": valid_actions,
        "partial_actions": partial_actions,
        "total_remaining_shortage":
            float(total_remaining_shortage),
    }