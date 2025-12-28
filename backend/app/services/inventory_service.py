# app/services/inventory_service.py
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from fastapi import HTTPException, status

class InventoryService:
    
    @staticmethod
    def add_stock(db: Session, transaction_in: TransactionCreate):
        # 1. Cari produknya
        product = db.query(Product).filter(Product.id == transaction_in.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

        # 2. Update stok produk
        product.stock += transaction_in.quantity

        # 3. Catat riwayat transaksi
        new_transaction = Transaction(
            product_id=transaction_in.product_id,
            transaction_type="IN",
            quantity=transaction_in.quantity
        )

        db.add(new_transaction)
        db.commit() # Menyimpan perubahan ke database
        db.refresh(product)
        return product

    @staticmethod
    def reduce_stock(db: Session, transaction_out: TransactionCreate):
        # 1. Cari produknya
        product = db.query(Product).filter(Product.id == transaction_out.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Produk tidak ditemukan")

        # 2. Validasi: Apakah stok cukup? (Penting untuk QA!)
        if product.stock < transaction_out.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Stok tidak cukup. Sisa stok: {product.stock}"
            )

        # 3. Update stok produk
        product.stock -= transaction_out.quantity

        # 4. Catat riwayat transaksi
        new_transaction = Transaction(
            product_id=transaction_out.product_id,
            type="OUT",
            quantity=transaction_out.quantity
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(product)
        return product