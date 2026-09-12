from models import Order, OrderItem, Customer
from utils.exceptions import *
from schemas.config import OrderStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.config import log
import asyncio


class OrderService:

    def __init__(self, db: Session):
        self.db = db

# ----------------------------------------------  

#  Order Service Utils

# ----------------------------------------------  

    async def _failed_paid_transaction(self, order_id):
        log.error("Failed to pay mony for this transaction")
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        order_obj.status = OrderStatus.FAILED.value
        self.db.commit()
    
    async def _success_paid_transaction(self, order_id):
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        order_obj.status = OrderStatus.PAID.value
        self.db.commit()

    async def _send_notification(self,order_id) -> None:
        # Call Shipping webhook
        log.info(f"Notification sent for order {order_id}")

    async def _save_accounting(self, order_id) -> None:
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        order_obj.status = OrderStatus.COMPLETED.value
        self.db.commit()
        log.info(f"Accounting saved for order {order_id}")

    async def _send_to_shipping(self, order_id) -> None:
        # Call Shipping webhook
        log.info(f"Order {order_id} sent to shipping")

    def _calculate_total(self, order_id) -> float:
        order_obj =  self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        return sum(
            item.total_order_price 
            for item in order_obj
        )
    
    async def _call_dargah_pardakht(self):
        # make request to darghah pardakht
        log.info("Start to connection to payment getway")
        await asyncio.sleep(3)
        log.info("Successfully called payment getway")

    async def _process_after_payment(self, order_id) -> None:
        steps = [
            self._send_notification,
            self._send_to_shipping,
            self._save_accounting,
        ]

        for step in steps:
            task = asyncio.create_task(step(order_id))
            task.add_done_callback(self._handle_task_result)


    def _handle_task_result(self, task):
        try:
            task.result()
        except Exception as e:
            log.error(f"Background task failed: {e}")

# --------------------------
# OrderService Busines Core
# --------------------------

    async def get_all_item(self):
        order_list =  self.db.scalars(
            select(Order)
        ).all()
        return {ord.id:{"CustomerID":ord.customer_id, "TotalPrice":ord.total_price, "OrderStatus":ord.status, "OrderCreationTime":ord.created_at} for ord in order_list}
        
    async def get_item(self, order_id: int):
        if order_id <= 0:
            raise ValueError("The cuorder_idstomer_id must  bigger than 0 ")
        order_obj =  self.db.get(Order, order_id)
        if not order_obj:
            raise ServiceException(f"The customer_id {order_obj} is not exist")
        
        return {
                "CustomerID":order_obj.customer_id, 
                "TotalPrice":order_obj.total_price, 
                "OrderStatus":order_obj.status, 
                "OrderCreationTime":order_obj.created_at
                } 
    
    async def add_new_empty_order(self, customer_id):
        """
        Add empty basket to initialize a new ordering process
        """
        if customer_id <= 0:
            raise ValueError("The customer_id must  bigger than 0 ")
        
        custome_obj =  self.db.get(Customer, customer_id)

        if not custome_obj:
            raise ServiceException(f"The customer_id {customer_id} is not exist")
        
        new_order = Order(
            customer_id=customer_id,
            created_at = datetime.now()
        )
        self.db.add(new_order)
        self.db.commit()
        return new_order

    async def remove_order(self, order_id):
        if order_id <= 0:
            raise ValueError("The order_id must  bigger than 0 ")
        
        order_obj =  self.db.get(Order, order_id)
        
        if not order_obj:
            raise ServiceException(f"The order_id {order_id} is not exist")
        
        self.db.delete(order_obj)

    async def cancel(self, order_id):
        if order_id <= 0:
            raise ValueError("The order_id must  bigger than 0 ")
        
        order_obj =  self.db.get(Order, order_id)

        if not order_obj:
            raise ServiceException(f"The order_id {order_id} is not exist")
        if  not order_obj.status == OrderStatus.PROCESSING.value:
            raise ServiceException(f"Can not to cancel order with status {order_obj.status} ")
        try:
            order_obj.status = OrderStatus.CANCELLED.value
            self.db.commit()
            log.debug(f"The orderid {order_id} was canceled by user ")
            self.db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
            self.db.commit()
            log.debug(f"The product of order id {order_id} was flushed from basket   ")
            # new method :)
            # from sqlalchemy import delete
            # self.db.execute(delete(OrderItem).where(OrderItem.order_id == order_id))
            # self.db.commit()
            return True
        except Exception as e:
            log.error(e)
            # log.error(e)
            return False
    
    async def complete(self, order_id):
        if order_id <= 0:
            raise ValueError("The order_id must  bigger than 0 ")
        
        order_obj =  self.db.get(Order, order_id)
        
        if not order_obj:
            raise ServiceException(f"The order_id {order_id} is not exist")
        
        if  not order_obj.status == OrderStatus.PAID.value:
            raise ServiceException(f"Can not to complete order with status {order_obj.status} ")
        try:
            order_obj.status = OrderStatus.COMPLETED.value
            self.db.commit()
            return True
        except Exception as e:
            # log.error(e)
            return False

    async def pay(self, order_id) -> None:
        if order_id <= 0:
            raise ValueError("The order_id must  bigger than 0 ")
        
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        
        if not order_obj:
            raise ServiceException(f"The order_id {order_id} is not exist")
        
        if  not order_obj.status == OrderStatus.PENDING.value:
            raise ServiceException(f"Can not to complete order with status {order_obj.status} ")
        
        
        log.debug(f"Order find with id {order_obj.id}")
        log.debug(f"Order status is {order_obj.status}")
        order_obj.status = OrderStatus.PROCESSING.value 
        self.db.commit()
        log.debug(f"Order status is {order_obj.status}")
        log.debug(f"Order total price is {order_obj.total_price}")
        order_obj.total_price = self._calculate_total(order_id)
        self.db.commit()
        log.debug(f"Order total price is {order_obj.total_price}")
        await self._call_dargah_pardakht()


    async def complete_payment(self, order_id, payment_status) -> None:
        """
        the payment operation successfully finish and products must to shiping
        """
        if order_id <= 0:
            raise ValueError("The order_id must  bigger than 0 ")
        
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        
        if not order_obj:
            raise ServiceException(f"The order_id {order_id} is not exist")
        
        if  not order_obj.status == OrderStatus.PROCESSING.value:
            raise ServiceException(f"Can not to complete order with status {order_obj.status} ")
        
        if payment_status :
            await self._success_paid_transaction(order_id)
            await self._process_after_payment(order_id)
        else:
            await self._failed_paid_transaction(order_id)
