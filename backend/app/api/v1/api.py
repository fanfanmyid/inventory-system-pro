from fastapi import APIRouter
from app.api.v1.endpoints import transactions, products,auth,sale # Import products

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(sale.router, prefix="/sales", tags=["Sales"])