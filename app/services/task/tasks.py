import asyncio

from services.order.order import OrderService
from services.order.order_items import OrderItemsService
from services.product.product import ProductService
from utils.database.connection import get_db

class Task:
    # create tasktype 
    # schadule task
    # run task
    # return task id


    # def __init__(self):
    #     self.task_id = task_id 

    def create_task(self, *args, **kwargs):
        pass
    def schadule_task(self, *args, **kwargs):
        pass
    def execute_task(self, *args, **kwargs):
        pass
    
# ----------------------------------------------


class RemoveProductFromBasketTasks:
    @staticmethod
    async def run(*args, **kwargs):
        product_id = kwargs.get("product_id")
        order_id = kwargs.get("order_id")

        with get_db() as db:
            return await OrderItemsService(db=db).remove_product_from_basket(order_id=order_id, product_id=product_id)

class AddProductToBasketTasks:
    @staticmethod
    async def run(*args, **kwargs):
        product_id = kwargs.get("product_id")
        product_count = kwargs.get("product_count")
        order_id = kwargs.get("order_id")

        with get_db() as db:
            return await OrderItemsService(db=db).add_product_to_basket(order_id=order_id, product_count=product_count, product_id=product_id)
# -----------------------------------------------------

class AddNewEmptyOrderTasks:
    @staticmethod
    async def run(*args, **kwargs):
        customer_id = kwargs.get("customer_id")

        with get_db() as db:
            return await OrderService(db=db).add_new_empty_order(customer_id=customer_id)


class GetOrdersTasks:
    # TODO -> for each request , do we need any new db obj
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await OrderService(db=db).get_all_item()
 
class GetOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            with get_db() as db:
                return await OrderService(db=db).get_item(kwargs.get("order_id"))

# ----------------------------------------------

class PayOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await OrderService(db=db).pay(kwargs.get("order_id"))


class CompletePaymentOperationTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await OrderService(db=db).complete_payment(order_id=kwargs.get("order_id"), payment_status=kwargs.get("payment_status"))

class CancelOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await OrderService(db=db).cancel(kwargs.get("order_id"))




# --------------------------------------

class GetProductsTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await ProductService(db=db).get_all_item()



class GetProductByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await ProductService(db=db).get_item(kwargs.get("product_id"))



class AddProductTasks:
    @staticmethod
    async def run(*args, **kwargs):
        name = kwargs.get("name")
        count = kwargs.get("count")
        price = kwargs.get("price")
        with get_db() as db:
            return await ProductService(db=db).add_item(name=name, count=count, price=price)

