from models import OrderItem, Product, Order
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from utils.exceptions import ServiceException
from schemas.config import OrderStatus


class OrderItemsService:

    def __init__(self, db: Session):
        self.db = db

    # ==================================================
    # Helpers
    # ==================================================

    def _change_item_quantity(
        self,
        order_id: int,
        product_id: int,
        quantity: int,
    ):
        result = self.db.execute(
            update(OrderItem)
            .where(
                OrderItem.order_id == order_id,
                OrderItem.product_id == product_id,
            )
            .values(quantity=quantity)
        )

        if result.rowcount != 1:
            raise ServiceException(
                "Order item does not exist"
            )

    def _delete_item(
        self,
        order_id: int,
        product_id: int,
    ):
        result = self.db.execute(
            delete(OrderItem)
            .where(
                OrderItem.order_id == order_id,
                OrderItem.product_id == product_id,
            )
        )

        if result.rowcount != 1:
            raise ServiceException(
                "Order item does not exist"
            )

    # ==================================================
    # Add Item
    # ==================================================

    async def add_item(
        self,
        product_id: int,
        order_id: int,
        product_count: int,
    ):
        """
        Add product to basket.
        """

        try:

            # ------------------------------------------
            # Get order and product
            # ------------------------------------------

            order = self.db.get(
                Order,
                order_id
            )

            product = self.db.get(
                Product,
                product_id
            )

            if not order:
                raise ServiceException(
                    f"Order {order_id} does not exist"
                )

            if not product:
                raise ServiceException(
                    f"Product {product_id} does not exist"
                )

            if order.status != OrderStatus.PENDING.value:
                raise ServiceException(
                    f"Can not add product when "
                    f"order status is {order.status}"
                )

            # ------------------------------------------
            # Atomic stock reservation
            # ------------------------------------------

            result = self.db.execute(
                update(Product)
                .where(
                    Product.id == product_id,
                    Product.count >= product_count,
                )
                .values(
                    count=Product.count - product_count
                )
            )

            if result.rowcount != 1:
                raise ServiceException(
                    "Not enough product in shop storage"
                )

            # ------------------------------------------
            # Create order item
            # ------------------------------------------

            order_item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=product_count,
                total_order_price=(
                    product_count * product.price
                ),
            )

            self.db.add(order_item)

            self.db.commit()

            return True

        except ServiceException:
            self.db.rollback()
            raise

        except Exception as e:
            self.db.rollback()
            raise ServiceException(
                f"Could not add product to basket: {e}"
            )

    # ==================================================
    # Remove Item
    # ==================================================

    async def remove_item(
        self,
        product_id: int,
        order_id: int,
        count: int,
    ):
        """
        Remove product from basket.
        """

        try:

            # ------------------------------------------
            # Get order
            # ------------------------------------------

            order = self.db.get(
                Order,
                order_id
            )

            if not order:
                raise ServiceException(
                    f"Order {order_id} does not exist"
                )

            if order.status != OrderStatus.PENDING.value:
                raise ServiceException(
                    f"Can not remove product when "
                    f"order status is {order.status}"
                )

            # ------------------------------------------
            # Get order item
            # ------------------------------------------

            order_item = self.db.scalars(
                select(OrderItem)
                .where(
                    OrderItem.order_id == order_id,
                    OrderItem.product_id == product_id,
                )
            ).first()

            if not order_item:
                raise ServiceException(
                    "Product does not exist in basket"
                )

            # ------------------------------------------
            # Check quantity
            # ------------------------------------------

            if count > order_item.quantity:
                raise ServiceException(
                    "Remove count is greater than "
                    "basket quantity"
                )

            # ------------------------------------------
            # Remove everything
            # ------------------------------------------

            if count == order_item.quantity:

                self._delete_item(
                    order_id,
                    product_id
                )

            # ------------------------------------------
            # Remove part of quantity
            # ------------------------------------------

            else:

                self._change_item_quantity(
                    order_id,
                    product_id,
                    order_item.quantity - count
                )

            # ------------------------------------------
            # Return stock
            # ------------------------------------------

            self.db.execute(
                update(Product)
                .where(Product.id == product_id)
                .values(
                    count=Product.count + count
                )
            )

            self.db.commit()

            return True

        except ServiceException:
            self.db.rollback()
            raise

        except Exception as e:
            self.db.rollback()
            raise ServiceException(
                f"Could not remove product from basket: {e}"
            )

