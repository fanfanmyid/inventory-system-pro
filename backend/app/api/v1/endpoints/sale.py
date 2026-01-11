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
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    size: int = 10
):
    # 1. Fetch data with joinedload
    query = db.query(Sale).options(
        joinedload(Sale.items).joinedload(SaleItem.product)
    )

    # ... (Keep your filter logic for name and dates here) ...

    total = query.count()
    offset = (page - 1) * size
    sales_objs = query.order_by(Sale.created_at.desc()).offset(offset).limit(size).all()

    # 2. THE FIX: Explicitly convert ORM objects to Schema objects
    # This prevents the "Unable to serialize unknown type" error
    items_to_return = []
    for sale in sales_objs:
        # validate_python or from_orm ensures Pydantic processes the SQLAlchemy object
        items_to_return.append(SaleResponse.model_validate(sale))

    return {
        "items": items_to_return, 
        "total": total,
        "page": page,
        "pages": (total + size - 1) // size
    }