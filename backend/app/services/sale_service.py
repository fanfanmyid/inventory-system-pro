import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sale import Sale, SaleItem
from app.schemas.sale import SaleItemCreate
from app.models.product import Product
from app.models.transaction import Transaction

class SaleService:
    @staticmethod
    def checkout(db: Session, sale_data: list[SaleItemCreate], current_user_id: int):
        total_price = 0.0
        sale_items = []
        
        # 1. Create Sale Header
        new_sale = Sale(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            user_id=current_user_id
        )
        db.add(new_sale)
        db.flush() # Get sale ID without committing yet

        for item in sale_data:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product or product.stock < item.quantity:
                db.rollback() # Cancel everything if one item fails
                raise HTTPException(status_code=400, detail=f"Stock low for {product.name if product else 'ID '+str(item.product_id)}")

            # 2. Update Product Stock
            product.stock -= item.quantity
            item_total = product.price * item.quantity
            total_price += item_total

            # 3. Create Sale Item
            sale_item = SaleItem(
                sale_id=new_sale.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price
            )
            sale_items.append(sale_item)

            # 4. Log to Transactions table for audit trail
            db.add(Transaction(
                product_id=product.id,
                transaction_type="OUT",
                quantity=item.quantity,
                reference=f"Sale {new_sale.invoice_number}"
            ))

        new_sale.total_price = total_price
        db.add_all(sale_items)
        db.commit()
        db.refresh(new_sale)
        return new_sale