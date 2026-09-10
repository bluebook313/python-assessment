from fastapi import APIRouter
from api.v1 import order_interface, product

router = APIRouter()
router.include_router(order_interface.router)
router.include_router(product.router, tags=["admin"])