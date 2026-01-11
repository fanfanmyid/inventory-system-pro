from datetime import datetime, time
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

# Database and Dependencies
from app.db.session import get_db
from app.api.deps import get_current_user

# Models (Direct File Imports)
from app.models.sale import Sale, SaleItem
from app.models.product import Product
from app.models.user import User

# Schemas and Services
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sale_service import SaleService

router = APIRouter()

@router.post("/", response_model=SaleResponse)
def create_sale(
    payload: SaleCreate, 
    db: Session = Depends(get_db),
    username: str = Depends(get_current_user)
):
    # Fetch User ID from the username provided by PASETO
    user = db.query(User).filter(User.username == username).first()
    return SaleService.checkout(db, payload.items, user.id)


@router.get("/", response_model=dict)
def get_sales_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    product_name: Optional[str] = None,
    invoice_number: Optional[str] = None, # New Search Param
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    size: int = 10
):
    # 1. Base Query with Joins
    query = db.query(Sale).options(
        joinedload(Sale.items).joinedload(SaleItem.product)
    )

    # 2. Apply Invoice Number Filter (Exact or Partial)
    if invoice_number:
        query = query.filter(Sale.invoice_number.ilike(f"%{invoice_number}%"))

    # 3. Apply Product Name Filter (Search inside nested items)
    if product_name:
        query = query.join(Sale.items).join(Product).filter(
            Product.name.ilike(f"%{product_name}%")
        ).distinct()

    # 4. Apply Date Filters with the 23:59 fix
    if start_date:
        start_dt = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d"), time.min)
        query = query.filter(Sale.created_at >= start_dt)
    
    if end_date:
        end_dt = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d"), time.max)
        query = query.filter(Sale.created_at <= end_dt)

    # 5. Pagination and Results
    total = query.count()
    offset = (page - 1) * size
    sales_objs = query.order_by(Sale.created_at.desc()).offset(offset).limit(size).all()

    items_to_return = []
    for sale in sales_objs:
        # Create a dictionary from the sale object
        sale_data = SaleResponse.model_validate(sale).model_dump()
        
        # Manually inject the product names into the items list
        for i, item_obj in enumerate(sale.items):
            if item_obj.product:
                sale_data['items'][i]['product_name'] = item_obj.product.name
        
        items_to_return.append(sale_data)

    # 6. Serialization
    items_to_return = [SaleResponse.model_validate(sale) for sale in sales_objs]

    return {
        "items": items_to_return, 
        "total": total,
        "page": page,
        "pages": (total + size - 1) // size
    }