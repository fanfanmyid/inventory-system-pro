from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional

class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"

class TransactionBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")
    transaction_type: TransactionType
    reference: Optional[str] = None # e.g., Supplier Name or Internal Note

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    product_name: Optional[str] = None

    class Config:
        from_attributes = True