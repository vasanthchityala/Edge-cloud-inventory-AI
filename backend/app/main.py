from fastapi import FastAPI

from backend.app.api.inventory import router as inventory_router
from backend.app.api.inventory_risk import (
    router as inventory_risk_router,
)
from backend.app.api.forecast import (
    router as forecast_router,
)
from backend.app.api.transfer import (
    router as transfer_router,
)
from backend.app.api.unified_priority import (
    router as unified_priority_router,
)
from backend.app.api.validated_action import (
    router as validated_action_router,
)
from backend.app.api.dashboard import (
    router as dashboard_router,
)
from backend.app.api.product import router as product_router
from backend.app.api.sale import router as sale_router
from backend.app.api.store import router as store_router


app = FastAPI(
    title="Edge-Cloud Inventory Intelligence Platform",
    version="0.1.0",
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(store_router)
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(sale_router)
app.include_router(inventory_risk_router)
app.include_router(forecast_router)
app.include_router(transfer_router)
app.include_router(unified_priority_router)
app.include_router(validated_action_router)
app.include_router(dashboard_router)

# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "project": "Edge-Cloud Inventory Intelligence Platform",
        "status": "running",
    }