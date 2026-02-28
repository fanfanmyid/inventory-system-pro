from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Direct File Imports
from app.models.transaction import Transaction
from app.models.product import Product
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.db.session import get_db
from app.services.transaction_service import TransactionService
from app.api.deps import get_current_user

from datetime import datetime,time
from typing import Optional

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_inventory_transaction(
    payload: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Standardized endpoint for creating inventory logs.
    """
    return TransactionService.process_transaction(db, payload)

@router.get("/", response_model=dict) # Changed to dict to return metadata + list
def get_transactions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    product_name: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = 1,
    size: int = 10
):
    # 1. Base Query with JOIN
    query = db.query(Transaction, Product.name.label("product_name")).join(Product)

    # 2. Filters
    if product_name:
        query = query.filter(Product.name.ilike(f"%{product_name}%"))
    if start_date:
        start_dt = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d"), time.min)
        query = query.filter(Transaction.created_at >= start_dt)
    # End Date: Force to 23:59:59
    if end_date:
        end_dt = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d"), time.max)
        query = query.filter(Transaction.created_at <= end_dt)

    # 3. Pagination Logic
    total_items = query.count()
    offset = (page - 1) * size
    results = query.order_by(Transaction.created_at.desc()).offset(offset).limit(size).all()

    # 4. Format Output
    transactions = []
    for tx, name in results:
        transactions.append({
            "id": tx.id,
            "product_id": tx.product_id,
            "product_name": name,
            "quantity": tx.quantity,
            "transaction_type": tx.transaction_type,
            "reference": tx.reference,
            "created_at": tx.created_at
        })

    return {
        "items": transactions,
        "total": total_items,
        "page": page,
        "size": size,
        "pages": (total_items + size - 1) // size
    }