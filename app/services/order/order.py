from datetime import datetime
import asyncio

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from models import Order, OrderItem, Customer
from utils.exceptions import ServiceException
from schemas.config import OrderStatus, log


class OrderService:

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------
    # Utils
    # --------------------------------------------------

    async def _failed_paid_transaction(self, order_id):
        log.error("Failed to pay money for this transaction")

        result = self.db.execute(
            update(Order)
            .where(
                Order.id == order_id,
            )
            .values(status=OrderStatus.FAILED.value)
        )

        self.db.commit()


    async def _success_paid_transaction(self, order_id):
        result = self.db.execute(
            update(Order)
            .where(
                Order.id == order_id
            )
            .values(status=OrderStatus.PAID.value)
        )

        self.db.commit()

    async def _send_notification(self, order_id):
        # Call customer that paied finished 
        log.info(f"Notification sent for order {order_id}")

    async def _save_accounting(self, order_id):
        self.db.execute(
            update(Order)
            .where(
                Order.id == order_id,
                Order.status == OrderStatus.PAID.value
            )
            .values(status=OrderStatus.COMPLETED.value)
        )

        self.db.commit()

        log.info(f"Accounting saved for order {order_id}")

    async def _send_to_shipping(self, order_id):
        # Call Shipping webhook
        log.info(f"Order {order_id} sent to shipping")

    def _calculate_total(self, order_id) -> float:
        items = self.db.scalars(
            select(OrderItem)
            .where(OrderItem.order_id == order_id)
        ).all()

        return sum(item.total_order_price for item in items)

    async def _call_dargah_pardakht(self):
        log.info("Start connection to payment gateway")

        await asyncio.sleep(3)

        log.info("Successfully called payment gateway")

    async def _process_after_payment(self, order_id):
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

    # --------------------------------------------------
    # Business Core
    # --------------------------------------------------

    async def get_all_item(self):

        orders = self.db.scalars(
            select(Order)
        ).all()

        return {
            order.id: {
                "CustomerID": order.customer_id,
                "TotalPrice": order.total_price,
                "OrderStatus": order.status,
                "OrderCreationTime": order.created_at,
            }
            for order in orders
        }

    async def get_item(self, order_id: int):

        if order_id <= 0:
            raise ServiceException(
                "The order_id must be bigger than 0"
            )

        order = self.db.get(Order, order_id)

        if not order:
            raise ServiceException(
                f"The order_id {order_id} does not exist"
            )

        return {
            "CustomerID": order.customer_id,
            "TotalPrice": order.total_price,
            "OrderStatus": order.status,
            "OrderCreationTime": order.created_at,
        }

    async def add_new_empty_order(self, customer_id):

        if customer_id <= 0:
            raise ServiceException(
                "The customer_id must be bigger than 0"
            )

        customer = self.db.get(Customer, customer_id)

        if not customer:
            raise ServiceException(
                f"The customer_id {customer_id} does not exist"
            )

        new_order = Order(
            customer_id=customer_id,
            created_at=datetime.now(),
        )

        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)

        return True

    async def remove_order(self, order_id):

        if order_id <= 0:
            raise ServiceException(
                "The order_id must be bigger than 0"
            )

        result = self.db.execute(
            delete(Order)
            .where(Order.id == order_id)
        )

        self.db.commit()

        if result.rowcount != 1:
            raise ServiceException(
                f"The order_id {order_id} does not exist"
            )

    async def cancel(self, order_id):

        if order_id <= 0:
            raise ServiceException(
                "The order_id must be bigger than 0"
            )

        # Atomic state transition 
        result = self.db.execute(
            update(Order)
            .where(
                Order.id == order_id,
                Order.status == OrderStatus.PROCESSING.value # check order status
            )
            .values(status=OrderStatus.CANCELLED.value)
        )

        if result.rowcount != 1:
            self.db.rollback()

            raise ServiceException(
                f"Can not cancel order {order_id}"
            )

        # Delete order items in the same transaction
        self.db.execute(
            delete(OrderItem)
            .where(OrderItem.order_id == order_id)
        )

        self.db.commit()

        log.info(
            f"Order {order_id} was cancelled by user"
        )

        return True

    async def complete(self, order_id):

        if order_id <= 0:
            raise ServiceException(
                "The order_id must be bigger than 0"
            )

        result = self.db.execute(
            update(Order)
            .where(
                Order.id == order_id,
                Order.status == OrderStatus.PAID.value # check order status
            )
            .values(status=OrderStatus.COMPLETED.value)
        )

        self.db.commit()

        if result.rowcount != 1:
            raise ServiceException(
                f"Can not complete order {order_id}"
            )

        return True

    async def pay(self, order_id):

        if order_id <= 0:
            raise ServiceException(
                "The order_id must be bigger than 0"
            )

        # --------------------------------------------------
        # 1. Calculate total
        # --------------------------------------------------

        total_price = self._calculate_total(order_id)

        # --------------------------------------------------
        # 2. Atomically:
        #    PENDING -> PROCESSING
        # --------------------------------------------------

        result = self.db.execute(
            update(Order)
            .where(
                Order.id == order_id,
                Order.status == OrderStatus.PENDING.value
            )
            .values(
                status=OrderStatus.PROCESSING.value,
                total_price=total_price,
            )
        )

        self.db.commit()

        # Nobody was able to transition the order
        if result.rowcount != 1:
            raise ServiceException(
                f"Can not process order {order_id}. "
                f"Order may already be processing."
            )

        log.debug(
            f"Order {order_id} changed to PROCESSING"
        )

        log.debug(
            f"Order {order_id} total price = {total_price}"
        )

        # --------------------------------------------------
        # 3. External payment
        # --------------------------------------------------

        await self._call_dargah_pardakht()

    async def complete_payment(
        self,
        order_id,
        payment_status
    ):

        if order_id <= 0:
            raise ServiceException(
                "The order_id must be bigger than 0"
            )

        if payment_status:

            await self._success_paid_transaction(order_id)

            await self._process_after_payment(order_id)

        else:

            await self._failed_paid_transaction(order_id)