from pydantic import BaseModel, Field


class InventoryCreate(BaseModel):
    store_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    current_stock: int = Field(ge=0)
    safety_stock: int = Field(ge=0)
    capacity: int = Field(gt=0)