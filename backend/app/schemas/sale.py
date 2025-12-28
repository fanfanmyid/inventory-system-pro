from pydantic import BaseModel
from typing import List
from datetime import datetime

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

class SaleCreate(BaseModel):
    items: List[SaleItemCreate]

class SaleResponse(BaseModel):
    id: int
    invoice_number: str
    total_price: float
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True