
from fastapi import APIRouter
from fastapi import status, HTTPException
from utils.api_response.response import CustoneResponse
router = APIRouter()

from services.task.tasks import ( GetOrdersTasks, GetOrderByIdTasks, 
                                  PayOrderByIdTasks, CancelOrderByIdTasks
                                )


async def handle_task(task_class, **kwargs):
    try:
        result =  await task_class.run(**kwargs)
        return CustoneResponse.response(
            status=status.HTTP_200_OK,
            details=f"task successfully submited - {result}"
        )       
    except Exception as e:
        return CustoneResponse.response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=str(e)
        )

@router.post("/orders")
async def get_orders():
    return await handle_task(task_class=GetOrdersTasks)


@router.get("/orders/{order_id}")
async def  get_order(order_id: int):
    return await handle_task(task_class=GetOrderByIdTasks, order_id=order_id)

@router.post("/orders/{order_id}/pay")
async def  pay_order(order_id: int):
    return await handle_task(task_class=PayOrderByIdTasks, order_id=order_id)

@router.post("/orders/{order_id}/cancel")
async def  cancel_order(order_id: int):
    return await handle_task(task_class=CancelOrderByIdTasks, order_id=order_id)
