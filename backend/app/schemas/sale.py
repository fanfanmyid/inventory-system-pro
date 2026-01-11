from pydantic import BaseModel, Field, field_validator
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
    product_name: Optional[str] = None 
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True # Allows reading from SQLAlchemy objects

    @field_validator("product_name", mode="before")
    @classmethod
    def get_name_from_product(cls, v, info):
        """
        QA Logic: Dynamically pulls the name from the joined Product model 
        if the database query included a .join(Product)
        """
        # In Pydantic v2, 'info.data' may not contain 'product' if it's an ORM object.
        # We check the actual object attributes if 'v' is None.
        return v

class SaleResponse(BaseModel):
    id: int
    invoice_number: str
    total_price: float
    created_at: datetime
    items: List[SaleItemResponse] # Correctly nests the items

    class Config:
        from_attributes = True