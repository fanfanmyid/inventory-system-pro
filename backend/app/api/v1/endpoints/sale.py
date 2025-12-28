from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sale_service import SaleService
from app.models.user import User

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