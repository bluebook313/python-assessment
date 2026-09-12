from fastapi import APIRouter
from fastapi import status as http_status
from utils.api_response.response import CustomResponse
router = APIRouter()

from services.task.tasks import GetCustomerInfoTasks, AddCustomerTasks
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

@router.get("/customer/{customer_id}")
async def  get_user_info(customer_id: int):
    return await handle_task(task_class=GetCustomerInfoTasks, customer_id=customer_id)

@router.post("/customer/add_customer/")
async def  add_customer(name:str, email:str): 
    return await handle_task(task_class=AddCustomerTasks, name=name, email=email)
