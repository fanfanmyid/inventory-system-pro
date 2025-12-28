from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    sku: str = Field(..., min_length=3, description="Unique Stock Keeping Unit")
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(default=0.0, ge=0)
    stock: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    # Note: We don't update stock here directly; 
    # stock changes should go through the Transaction module.

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True