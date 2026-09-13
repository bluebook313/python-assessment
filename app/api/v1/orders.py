
from fastapi import APIRouter
from fastapi import status as http_status
from utils.api_response.response import CustomResponse
from schemas.schema import OrderItemStructure
router = APIRouter()

from services.task.tasks import ( GetOrdersTasks, GetOrderByIdTasks, 
                                  PayOrderByIdTasks, CancelOrderByIdTasks,
                                  AddNewEmptyOrderTasks, AddProductToBasketTasks,
                                  RemoveProductFromBasketTasks, CompletePaymentOperationTasks,
                                )

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

@router.post("/orders")
async def get_orders():
    return await handle_task(task_class=GetOrdersTasks)


@router.get("/orders/{order_id}")
async def  get_order(order_id: int):
    if order_id<=0:
        return CustomResponse.response(
                status=http_status.HTTP_400_BAD_REQUEST,
                details="input must bigger than 0",
                result={},
    )
    return await handle_task(task_class=GetOrderByIdTasks, order_id=order_id)

@router.post("/orders/add_new_empty_order")
async def  add_new_empty_order(customer_id:int):
    if customer_id<=0:
        return CustomResponse.response(
                status=http_status.HTTP_400_BAD_REQUEST,
                details="input must bigger than 0",
                result={},
    )
    return await handle_task(task_class=AddNewEmptyOrderTasks, customer_id = customer_id)

@router.post("/orders/add_product_to_basket")
async def  add_product_to_basket(order_item_param: OrderItemStructure):
    if order_item_param.order_id<=0 or order_item_param.product_count<=0 or order_item_param.product_id<=0:
        return CustomResponse.response(
                status=http_status.HTTP_400_BAD_REQUEST,
                details="input must bigger than 0",
                result={},
    )
    return await handle_task(   
                            task_class=AddProductToBasketTasks, 
                            order_id=order_item_param.order_id, 
                            product_count=order_item_param.product_count, 
                            product_id=order_item_param.product_id
                            )

@router.post("/orders/remove_product_from_basket")
async def  remove_product_from_basket(product_id:int, order_id:int, count:int):
    if order_id<=0 or product_id<=0 or count<=0:
        return CustomResponse.response(
                status=http_status.HTTP_400_BAD_REQUEST,
                details="input must bigger than 0",
                result={},
    )
    return await handle_task(   
                            task_class=RemoveProductFromBasketTasks, 
                            order_id=order_id, 
                            product_id=product_id,
                            count=count
                            )

@router.post("/orders/{order_id}/pay")
async def  pay_order(order_id: int):
    if order_id<=0 :
        return CustomResponse.response(
                status=http_status.HTTP_400_BAD_REQUEST,
                details="input must bigger than 0",
                result={},
    )
    return await handle_task(task_class=PayOrderByIdTasks, order_id=order_id)

@router.post("/orders/{order_id}/pay_web_hook_answer")
async def  complete_pay_operation(order_id: int, payment_status:bool):
    if order_id<=0:
        return CustomResponse.response(
                status=http_status.HTTP_400_BAD_REQUEST,
                details="input must bigger than 0",
                result={},
    )
    return await handle_task(task_class=CompletePaymentOperationTasks, order_id=order_id, payment_status=payment_status)

@router.post("/orders/{order_id}/cancel")
async def  cancel_order(order_id: int):
    if order_id<=0 :
        return CustomResponse.response(
                status=http_status.HTTP_400_BAD_REQUEST,
                details="input must bigger than 0",
                result={},
    )
    return await handle_task(task_class=CancelOrderByIdTasks, order_id=order_id)
