from fastapi import APIRouter
from fastapi import status, HTTPException
from utils.api_response.response import CustoneResponse
router = APIRouter()

from services.task.tasks import GetCustomerInfoTasks, AddCustomerTasks
                        


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

@router.get("/customer/{customer_id}")
async def  get_user_info(customer_id: int):
    return await handle_task(task_class=GetCustomerInfoTasks, customer_id=customer_id)

@router.post("/customer/add_customer/")
async def  add_customer(name:str, email:str): 
    return await handle_task(task_class=AddCustomerTasks, name=name, email=email)
