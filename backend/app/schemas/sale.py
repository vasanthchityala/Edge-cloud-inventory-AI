from datetime import date

from pydantic import BaseModel, Field


class SaleCreate(BaseModel):
    store_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    sale_date: date
    quantity: int = Field(gt=0)