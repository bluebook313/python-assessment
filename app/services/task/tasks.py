import asyncio

from services.order.order import Order
from services.product.product import Product

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
    @staticmethod
    async def run(*args, **kwargs):
        return await Order().get_all_item()
 
class GetOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        return await Order().get_item(kwargs.get("order_id"))

class PayOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        return await Order().pay(kwargs.get("order_id"))

class CancelOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        return await Order().cancel(kwargs.get("order_id"))



class GetProductsTasks:
    @staticmethod
    async def run(*args, **kwargs):
        return await Product().get_all_item()



class GetProductByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        return await Product().get_item(kwargs.get("product_id"))

