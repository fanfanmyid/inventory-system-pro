from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, default=0.0)
    stock = Column(Integer, default=0) # Stock level saat ini