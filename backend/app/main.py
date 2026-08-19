from fastapi import FastAPI

from backend.app.api.inventory import router as inventory_router
from backend.app.api.product import router as product_router
from backend.app.api.sale import router as sale_router
from backend.app.api.store import router as store_router


app = FastAPI(
    title="Edge-Cloud Inventory Intelligence Platform",
    version="0.1.0",
)


app.include_router(store_router)
app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(sale_router)


@app.get("/")
def root():
    return {
        "project": "Edge-Cloud Inventory Intelligence Platform",
        "status": "running",
    }