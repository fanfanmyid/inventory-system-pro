from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=TransactionResponse)
def create_inventory_transaction(
    payload: TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    General endpoint for Stock In and Stock Out.
    Standardized for inventory entry and exit logs.
    """
    return TransactionService.process_transaction(db, payload)