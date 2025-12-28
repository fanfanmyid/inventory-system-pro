from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from fastapi import HTTPException

class ProductService:
    @staticmethod
    def get_products(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: str = None,
        min_stock: int = None,
        sort_by: str = "name",
        order: str = "asc"
    ):
        query = db.query(Product)

        # 1. Filtering Logic
        if search:
            # Search in both Name and SKU
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.sku.ilike(f"%{search}%")
                )
            )
        
        if min_stock is not None:
            query = query.filter(Product.stock >= min_stock)

        # 2. Sorting Logic
        # Map strings to actual model columns
        sort_column = getattr(Product, sort_by, Product.name)
        if order.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_product(db: Session, product_in: ProductCreate):
        # Check if SKU already exists
        existing_product = db.query(Product).filter(Product.sku == product_in.sku).first()
        if existing_product:
            raise HTTPException(status_code=400, detail="SKU already registered")
        
        db_product = Product(**product_in.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update_product(db: Session, product_id: int, product_in: ProductUpdate):
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
            
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def get_product(db: Session, product_id: int):
        """
        Fetches a single product by its unique ID.
        Returns None if not found.
        """
        return db.query(Product).filter(Product.id == product_id).first()