from datetime import datetime
import asyncio

from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from models import Order, OrderItem, Customer
from utils.exceptions import ServiceException
from schemas.config import OrderStatus, log


class OrderService:

    def __init__(self, db: Session):
        self.db  = db

    # ==================================================
    # Transaction Helper
    # ==================================================

    async def _rollback(self):
        try:
            await self.db.rollback()
        except Exception as e:
            log.error(f"Rollback failed: {e}")

    async def _change_status(
        self,
        order_id: int,
        from_status: str,
        to_status: str,
    ):
        try:
            result = await self.db.execute(
                update(Order)
                .where(
                    Order.id == order_id,
                    Order.status == from_status,
                )
                .values(status=to_status)
            )

            if result.rowcount != 1:
                raise ServiceException(
                    f"Can not change order {order_id} "
                    f"from {from_status} to {to_status}"
                )

            return result

        except ServiceException:
            raise

        except Exception as e:
            log.error(
                f"Database error while changing order "
                f"{order_id}: {e}"
            )
            raise ServiceException(
                "Database error while changing order"
            )

    async def _delete_order_items(self, order_id: int):

        try:
            await self.db.execute(
                delete(OrderItem)
                .where(OrderItem.order_id == order_id)
            )

        except Exception as e:
            log.error(
                f"Error deleting items of order "
                f"{order_id}: {e}"
            )
            raise ServiceException(
                "Could not delete order items"
            )

    async def _delete_order(self, order_id: int):

        try:
            result = await self.db.execute(
                delete(Order)
                .where(Order.id == order_id)
            )

            if result.rowcount != 1:
                raise ServiceException(
                    f"Order {order_id} does not exist"
                )

        except ServiceException:
            raise

        except Exception as e:
            log.error(
                f"Error deleting order {order_id}: {e}"
            )
            raise ServiceException(
                "Could not delete order"
            )

    async def _calculate_total(self, order_id: int) -> float:

        try:
            items = await self.db.scalars(
                select(OrderItem)
                .where(OrderItem.order_id == order_id)
            )
            items = items.all()

            return sum(
                item.total_order_price
                for item in items
            )

        except Exception as e:
            log.error(
                f"Error calculating order total "
                f"{order_id}: {e}"
            )
            raise ServiceException(
                "Could not calculate order total"
            )

    # ==================================================
    # Payment
    # ==================================================

    async def _failed_paid_transaction(self, order_id):

        log.error(
            "Failed to pay money for this transaction"
        )

        try:
            await self._change_status(
                order_id,
                OrderStatus.PROCESSING.value,
                OrderStatus.FAILED.value,
            )

            await self.db.commit()

        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Failed payment transaction "
                f"for order {order_id}: {e}"
            )

            raise ServiceException(
                "Failed to update payment status"
            )

    async def _success_paid_transaction(self, order_id):

        try:
            await self._change_status(
                order_id,
                OrderStatus.PROCESSING.value,
                OrderStatus.PAID.value,
            )

            await self.db.commit()

        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Failed to complete payment "
                f"for order {order_id}: {e}"
            )

            raise ServiceException(
                "Failed to update payment status"
            )

    # ==================================================
    # Background Operations
    # ==================================================

    async def _send_notification(self, order_id):

        try:
            log.info(
                f"Notification sent for order {order_id}"
            )

        except Exception as e:
            log.error(
                f"Notification failed for order "
                f"{order_id}: {e}"
            )
            raise

    async def _send_to_shipping(self, order_id):

        try:
            log.info(
                f"Order {order_id} sent to shipping"
            )

        except Exception as e:
            log.error(
                f"Shipping failed for order "
                f"{order_id}: {e}"
            )
            raise

    async def _save_accounting(self, order_id):

        try:
            await self._change_status(
                order_id,
                OrderStatus.PAID.value,
                OrderStatus.COMPLETED.value,
            )

            await self.db.commit()

            log.info(
                f"Accounting saved for order {order_id}"
            )

        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Accounting failed for order "
                f"{order_id}: {e}"
            )

            raise ServiceException(
                "Failed to save accounting"
            )

    async def _process_after_payment(self, order_id):

        steps = [
            self._send_notification,
            self._send_to_shipping,
            self._save_accounting,
        ]

        for step in steps:

            task = asyncio.create_task(
                step(order_id)
            )

            task.add_done_callback(
                self._handle_task_result
            )

    def _handle_task_result(self, task):

        try:
            task.result()

        except Exception as e:
            log.error(
                f"Background task failed: {e}"
            )

    async def _call_dargah_pardakht(self):

        try:
            log.info(
                "Start connection to payment gateway"
            )

            await asyncio.sleep(3)

            log.info(
                "Successfully called payment gateway"
            )

        except Exception as e:
            log.error(
                f"Payment gateway error: {e}"
            )
            raise ServiceException(
                "Payment gateway failed"
            )

    # ==================================================
    # Query
    # ==================================================

    async def get_all_item(self):

        try:
            orders = await self.db.scalars(
                select(Order)
            )
            orders= orders.all()

            return {
                order.id: {
                    "CustomerID": order.customer_id,
                    "TotalPrice": order.total_price,
                    "OrderStatus": order.status,
                    "OrderCreationTime": str(order.created_at),
                }
                for order in orders
            }

        except Exception as e:
            log.error(
                f"Error getting orders: {e}"
            )
            raise ServiceException(
                "Could not get orders"
            )

    async def get_item(self, order_id: int):

        try:
            order = await self.db.get(
                Order,
                order_id
            )

            if not order:
                raise ServiceException(
                    f"Order {order_id} does not exist"
                )

            return {
                "OrderId": order.id,
                "CustomerID": order.customer_id,
                "TotalPrice": order.total_price,
                "OrderStatus": order.status,
                "OrderCreationTime": str(order.created_at),
            }

        except ServiceException:
            raise

        except Exception as e:
            log.error(
                f"Error getting order "
                f"{order_id}: {e}"
            )
            raise ServiceException(
                "Could not get order"
            )

    # ==================================================
    # Create
    # ==================================================

    async def add_new_empty_order(
        self,
        customer_id: int
    ):

        try:
            customer = await self.db.get(
                Customer,
                customer_id
            )

            if not customer:
                raise ServiceException(
                    f"Customer {customer_id} does not exist"
                )

            order = Order(
                customer_id=customer_id,
                created_at=datetime.now(),
            )

            self.db.add(order)

            await self.db.commit()

            return {
                "Id":order.id
            }

        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Error creating order: {e}"
            )

            raise ServiceException(
                "Could not create order"
            )

    # ==================================================
    # Delete
    # ==================================================

    async def remove_order(self, order_id: int):

        try:
            
            await self._delete_order(order_id)

            await self.db.commit()
            return {"Id":order_id}

        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Error removing order "
                f"{order_id}: {e}"
            )

            raise ServiceException(
                "Could not remove order"
            )

    # ==================================================
    # Cancel
    # ==================================================

    async def cancel(self, order_id: int):

        try:

            await self._change_status(
                order_id,
                OrderStatus.PENDING.value,
                OrderStatus.CANCELLED.value,
            )
            
            await self._delete_order_items(order_id)

            await self.db.commit()

            log.debug(
                f"Order {order_id} was cancelled"
            )

            return {"Id":order_id}

        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Error cancelling order "
                f"{order_id}: {e}"
            )

            raise ServiceException(
                "Could not cancel order"
            )

    # ==================================================
    # Complete
    # ==================================================

    async def complete(self, order_id: int):

        try:

            await self._change_status(
                order_id,
                OrderStatus.PAID.value,
                OrderStatus.COMPLETED.value,
            )

            await self.db.commit()

            return {"Id":order_id}

        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Error completing order "
                f"{order_id}: {e}"
            )

            raise ServiceException(
                "Could not complete order"
            )

    # ==================================================
    # Pay
    # ==================================================

    async def pay(self, order_id: int):

        try:

            total_price = await self._calculate_total(
                order_id
            )

            result = await self.db.execute(
                update(Order)
                .where(
                    Order.id == order_id,
                    Order.status == OrderStatus.PENDING.value,
                )
                .values(
                    status=OrderStatus.PROCESSING.value,
                    total_price=total_price,
                )
            )

            if result.rowcount != 1:
                raise ServiceException(
                    f"Can not process order {order_id}"
                )

            await self.db.commit()

            log.debug(
                f"Order {order_id} changed to PROCESSING"
            )

            log.debug(
                f"Order {order_id} total price = "
                f"{total_price}"
            )
            return {"Id":order_id}
        
        except ServiceException:
            await self._rollback()
            raise

        except Exception as e:
            await self._rollback()

            log.error(
                f"Error processing order "
                f"{order_id}: {e}"
            )

            raise ServiceException(
                "Could not process order"
            )

        await self._call_dargah_pardakht()

    # ==================================================
    # Complete Payment
    # ==================================================

    async def complete_payment(
        self,
        order_id: int,
        payment_status: bool,
    ):

        if payment_status:

            await self._success_paid_transaction(
                order_id
            )

            await self._process_after_payment(
                order_id
            )
            return {"Id":order_id}
        else:

            await self._failed_paid_transaction(
                order_id
            )
            return {"Id":order_id}

