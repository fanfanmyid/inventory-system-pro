from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionType
from fastapi import HTTPException, status

class TransactionService:
    @staticmethod
    def process_transaction(db: Session, data: TransactionCreate):
        # 1. Verify Product exists
        product = db.query(Product).filter(Product.id == data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # 2. Logic for Stock Out (Validation)
        if data.transaction_type == TransactionType.OUT:
            if product.stock < data.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock. Current balance: {product.stock}"
                )
            product.stock -= data.quantity
        
        # 3. Logic for Stock In
        else:
            product.stock += data.quantity

        # 4. Save Log
        # Inside process_transaction method:
        db_transaction = Transaction(
            product_id=data.product_id,
            transaction_type=data.transaction_type,
            quantity=data.quantity,
            reference=data.reference
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(product)
        return db_transaction