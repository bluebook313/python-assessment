from fastapi import APIRouter
from fastapi import status, HTTPException
from utils.api_response.response import CustoneResponse
router = APIRouter()

from services.task.tasks import GetProductsTasks, GetProductByIdTasks, AddProductTasks
from schemas.schema import  ProductStructure                           


async def handle_task(task_class, **kwargs):
    try:
        result =  await task_class.run(**kwargs)
        return CustoneResponse.response(
            status=status.HTTP_200_OK,
            details=f"task successfully submited",
            result = result
        )       
    except Exception as e:
        return CustoneResponse.response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(e),
            result={}
        )

@router.post("/products")
async def get_products():
    return await handle_task(task_class=GetProductsTasks)


@router.get("/products/{product_id}")
async def  get_product(product_id: int):
    return await handle_task(task_class=GetProductByIdTasks, product_id=product_id)

@router.post("/products/add_product/")
async def  add_products(params:ProductStructure): 
    return await handle_task(task_class=AddProductTasks, name=params.name, count=params.product_count, price=params.price)
