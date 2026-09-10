
from fastapi import APIRouter
from fastapi import status, HTTPException
router = APIRouter()




@router.post("/orders")
def get_orders():
    return {}


@router.get("/orders/{id}")
def get_order(id: int):
    return {}

@router.post("/orders/{id}/pay")
def get_order(id: int):
    return {}

@router.post("/orders/{id}/cancel")
def get_order(id: int):
    return {}


