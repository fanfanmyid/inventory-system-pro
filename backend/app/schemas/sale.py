from pydantic import BaseModel, Field, field_validator,ConfigDict
from datetime import datetime
from typing import List, Optional

# --- INPUT SCHEMAS (Used for POST) ---

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0) # QA Rule: prevents zero/negative sales
    unit_price: float

class SaleCreate(BaseModel):
    invoice_number: str
    items: List[SaleItemCreate]
    total_price: float


# --- OUTPUT SCHEMAS (Used for GET/Response) ---

class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str  # Pydantic will now find this in the @property
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)

class SaleResponse(BaseModel):
    id: int
    invoice_number: str
    total_price: float
    created_at: datetime
    items: List[SaleItemResponse]

    model_config = ConfigDict(from_attributes=True)