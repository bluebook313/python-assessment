
from fastapi import APIRouter
from fastapi import status, HTTPException
router = APIRouter()




@router.get("/products")
def get_products():
    return {}


@router.get("/products/{id}")
def get_product(id: int):
    return {}