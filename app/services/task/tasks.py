import asyncio

from services.order.order import OrderService
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

class PayOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await OrderService().pay(kwargs.get("order_id"))

class CancelOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        with get_db() as db:
            return await OrderService().cancel(kwargs.get("order_id"))



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

