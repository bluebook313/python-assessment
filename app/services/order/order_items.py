from models import OrderItem, Product
from sqlalchemy.orm import Session



class OrderItemsService:

    def __init__(self, db: Session):
        self.db = db

    async def add_item(self, product_id, order_id, product_count):
        """
        add product to basket
        """
        product_obj =  self.db.get(Product, product_id)
        new_order = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=product_count,
            total_order_price = product_count * product_obj.price
        )
        self.db.add(new_order)
        self.db.commit()
        return new_order

    async def remove_item(self, product_id, order_id, count):
        """
        remove product from basket
        """
        order_obj = self.db.query(OrderItem).filter(OrderItem.product_id == product_id and OrderItem.order_id == order_id).first()
        if count > order_obj.quantity:
            raise Exception("The product count that you want to remove from basket is more than of quantity of product in basket")
        if count < order_obj.quantity:
            order_obj.quantity -= count
            self.db.commit()
        if count == order_obj.quantity:
            self.db.delete(order_obj)
            self.db.commit()

