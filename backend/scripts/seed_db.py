import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Import your models
from app.models.user import User
from app.models.product import Product # Ensure this path is correct

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/inventory_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    db = SessionLocal()
    try:
        # 1. Seed User
        if not db.query(User).filter(User.username == "fanfanmyid").first():
            USERNAME_SEED = os.getenv("USERNAME_SEED")
            PASSWORD_SEED = os.getenv("PASSWORD_SEED")
            db.add(User(
                username=USERNAME_SEED,
                hashed_password=pwd_context.hash(PASSWORD_SEED)
            ))
            print("--- Seed: User created ---")

        # 2. Seed Products
        initial_products = [
            {"sku": "MTR-CB150X", "name": "Honda CB150X", "price": 35000000, "stock": 10},
            {"sku": "MTR-SATRIA", "name": "Suzuki Satria FU", "price": 28000000, "stock": 5},
            {"sku": "ACC-HLMT", "name": "Fullface Helmet", "price": 1500000, "stock": 20}
        ]

        for p_data in initial_products:
            if not db.query(Product).filter(Product.sku == p_data["sku"]).first():
                db.add(Product(**p_data))
                print(f"--- Seed: Product {p_data['sku']} created ---")
        
        db.commit()
    except Exception as e:
        print(f"--- Seed Error: {e} ---")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()