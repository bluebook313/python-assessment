from models import Order, OrderItem
from schemas.config import OrderStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio


class OrderService:

    def __init__(self, db: Session):
        self.db = db

    async def get_all_item(self):
        order_list =  self.db.scalars(
            select(Order)
        ).all()
        return {ord.id:{"CustomerID":ord.customer_id, "TotalPrice":ord.total_price, "OrderStatus":ord.status, "OrderCreationTime":ord.created_at} for ord in order_list}
        
    async def get_item(self, order_id: int):
        order_obj =  self.db.get(Order, order_id)
        return {
                "CustomerID":order_obj.customer_id, 
                "TotalPrice":order_obj.total_price, 
                "OrderStatus":order_obj.status, 
                "OrderCreationTime":order_obj.created_at
                } 
    
    async def add_new_empty_order(self, customer_id):
        """
        when the user add all product to the basket 
        and want to close the order and regester the order
        """
        new_order = Order(
            customer_id=customer_id,
            created_at = datetime.now()
        )
        self.db.add(new_order)
        self.db.commit()
        return new_order

    async def remove_order(self, order_id):
        order_obj =  self.db.get(Order, order_id)
        self.db.delete(order_obj)

    async def cancel(self, order_id):
        try:
            order_obj =  self.db.get(Order, order_id)
            order_obj.status = OrderStatus.CANCELLED.value
            self.db.commit()
            print(f"The orderid {order_id} was csnceled by user ")
            self.db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
            self.db.commit()
            print(f"The product of order id {order_id} was flushed from basket   ")
            # new method :)
            # from sqlalchemy import delete
            # self.db.execute(delete(OrderItem).where(OrderItem.order_id == order_id))
            # self.db.commit()
            return True
        except Exception as e:
            print(e)
            # log.error(e)
            return False
    
    async def complete(self, order_id):
        try:
            order_obj =  self.db.get(Order, order_id)
            order_obj.status = OrderStatus.COMPLETED.value
            self.db.commit()
            return True
        except Exception as e:
            # log.error(e)
            return False


    def calculate_total(self, order_id) -> float:
        order_obj =  self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        return sum(
            item.total_order_price 
            for item in order_obj
        )

    async def pay(self, order_id) -> None:
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        print(f"Order find with id {order_obj.id}")
        print(f"Order status is {order_obj.status}")
        order_obj.status = OrderStatus.PROCESSING.value 
        self.db.commit()
        print(f"Order status is {order_obj.status}")
        print(f"Order total price is {order_obj.total_price}")
        order_obj.total_price = self.calculate_total(order_id)
        self.db.commit()
        print(f"Order total price is {order_obj.total_price}")
        await self.call_dargah_pardakht()

        

    async def complete_payment(self, order_id, payment_status) -> None:
        """
        the payment operation successfully finish and products must to shiping
        """
        if payment_status :
            await self.success_paid_transaction(order_id)
            await self.process_after_payment(order_id)
        else:
            await self.failed_paid_transaction(order_id)
        

    async def failed_paid_transaction(self, order_id):
        print("failed to pay mony for this transaction")
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        order_obj.status = OrderStatus.FAILED.value
        self.db.commit()
    
    async def success_paid_transaction(self, order_id):
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        order_obj.status = OrderStatus.PAID.value
        self.db.commit()

    async def send_notification(self,order_id) -> None:
        # Call Shipping webhook
        print(f"Notification sent for order {order_id}")

    async def save_accounting(self, order_id) -> None:
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        order_obj.status = OrderStatus.COMPLETED.value
        self.db.commit()
        print(f"Accounting saved for order {order_id}")

    async def send_to_shipping(self, order_id) -> None:
        # Call Shipping webhook
        print(f"Order {order_id} sent to shipping")

    async def process_after_payment(self,order_id) -> None:
        steps =[
            self.send_notification,
            self.send_to_shipping,
            self.save_accounting
        ]

        for step in steps:
            try:
                print(f"Try to execute step {step.__name__}")
                await step(order_id)
            except Exception as e:
                print(f"The error is in step {step.__name__} - details is : {e}")


    async def call_dargah_pardakht(self):
        # make request to darghah pardakht
        print("Start to connection to payment getway")
        await asyncio.sleep(3)