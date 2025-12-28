from fastapi import APIRouter, Depends, Query,HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from typing import List, Optional
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search by name or SKU"),
    min_stock: Optional[int] = Query(None, description="Filter items with stock >= this value"),
    sort_by: str = Query("name", enum=["name", "price", "stock", "sku"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    current_user: str = Depends(get_current_user)
):
    """
    Retrieve products with optional filtering and sorting.
    Example: /products/?search=keyboard&min_stock=5&sort_by=price&order=desc
    """
    return ProductService.get_products(
        db, 
        skip=skip, 
        limit=limit, 
        search=search, 
        min_stock=min_stock, 
        sort_by=sort_by, 
        order=order
    )

@router.post("/", response_model=ProductResponse)
def create_product(
    payload: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
    ):
    return ProductService.create_product(db, payload)

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    return ProductService.update_product(db, product_id, payload)

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(
    product_id: int, 
    db: Session = Depends(get_db),
    # Keep this protected so only logged-in users can see details
    current_user: str = Depends(get_current_user) 
):
    product = ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product