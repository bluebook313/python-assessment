import asyncio

from services.order.order import OrderService
from services.order.order_items import OrderItemsService
from services.product.product import ProductService
from services.customer.customer import CustomerService
from utils.database.connection import AsyncSessionLocal

class GetCustomerInfoTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await CustomerService(db=db).get_customer_info(**kwargs)



class AddCustomerTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await CustomerService(db=db).add_customer(**kwargs)


# ----------------------------------------------


class RemoveProductFromBasketTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderItemsService(db=db).remove_item(**kwargs)

class AddProductToBasketTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderItemsService(db=db).add_item(**kwargs)


class AddNewEmptyOrderTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderService(db=db).add_new_empty_order(**kwargs)

# -----------------------------------------------------

class GetOrdersTasks:
    # TODO -> for each request , do we need any new db obj
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderService(db=db).get_all_item()
 
class GetOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderService(db=db).get_item(**kwargs)

# ----------------------------------------------

class PayOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderService(db=db).pay(**kwargs)


class CompletePaymentOperationTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderService(db=db).complete_payment(**kwargs)

class CancelOrderByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await OrderService(db=db).cancel(**kwargs)




# --------------------------------------

class GetProductsTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await ProductService(db=db).get_all_item()



class GetProductByIdTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await ProductService(db=db).get_item(**kwargs)


class AddProductTasks:
    @staticmethod
    async def run(*args, **kwargs):
        async with AsyncSessionLocal() as db:
            return await ProductService(db=db).add_item(**kwargs)

