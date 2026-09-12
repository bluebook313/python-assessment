from fastapi import APIRouter
from fastapi import status as http_status
from utils.api_response.response import CustomResponse
router = APIRouter()

from services.task.tasks import GetProductsTasks, GetProductByIdTasks, AddProductTasks
from schemas.schema import  ProductStructure                           

from utils.exceptions import ServiceException                       


async def handle_task(task_class, **kwargs):
    try:
        result = await task_class.run(**kwargs)

        return CustomResponse.response(
            status=http_status.HTTP_200_OK,
            details="Task successfully submitted",
            result=result,
        )

    except ServiceException as e:
        status = http_status.HTTP_400_BAD_REQUEST
        details = str(e)

    except Exception as e:
        status = http_status.HTTP_500_INTERNAL_SERVER_ERROR
        details = str(e)

    return CustomResponse.response(
        status=status,
        details=details,
        result={},
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
