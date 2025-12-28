from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    total_price = Column(Float, default=0.0)
    # --- Association with User ---
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    # -----------------------------
    items = relationship("SaleItem", back_populates="sale")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SaleItem(Base):
    __tablename__ = "sale_items"
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float) # Store price at time of sale
    
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")