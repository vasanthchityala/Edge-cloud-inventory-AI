from datetime import datetime

from pydantic import BaseModel, Field


class TransferResponse(BaseModel):
    id: int
    from_store_id: int
    to_store_id: int
    product_id: int
    quantity: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TransferCreate(BaseModel):
    from_store_id: int
    to_store_id: int
    product_id: int
    quantity: int = Field(gt=0)
    status: str = "recommended"