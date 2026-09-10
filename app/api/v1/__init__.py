from fastapi import APIRouter
from api.v1 import orders, product

router = APIRouter()
router.include_router(orders.router, tags=["orders"])
router.include_router(product.router, tags=["product"])