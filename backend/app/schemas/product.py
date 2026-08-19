from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str
    unit_price: Decimal = Field(gt=0)