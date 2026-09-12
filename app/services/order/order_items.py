from models import OrderItem, Product, Order
from sqlalchemy.orm import Session
from utils.exceptions import *
from schemas.config import OrderStatus


class OrderItemsService:

    def __init__(self, db: Session):
        self.db = db

    async def add_item(self, product_id, order_id, product_count):
        """
        add product to basket
        """
        if order_id <= 0 or product_id<=0 or product_count<=0:
            raise ServiceException("The order_id or product_id or product_count  must  bigger than 0 ")
        
        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        product_obj =  self.db.query(Product).filter(Product.id == product_id).first()

        if not order_obj:
            raise ServiceException(f"The order_id {order_id} is not exist")      
        
        if not product_obj:
            raise ServiceException(f"The product_id {product_id} is not exist")
        if product_obj.count < product_count:
            raise ServiceException(f"The {product_count} is not exist in Shop Storage") 
        
        if  not order_obj.status == OrderStatus.PENDING.value:
            raise ServiceException(f"Can not to add product to basket when order with status {order_obj.status} ")

        new_order = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=product_count,
            total_order_price = product_count * product_obj.price
        )
        self.db.add(new_order)
        self.db.commit()
        return True

    async def remove_item(self, product_id, order_id, count):
        """
        remove product from basket
        """
        if order_id <= 0 or product_id<=0 or count<=0:
            raise ServiceException("The order_id or product_id or count  must  bigger than 0 ")

        order_obj =  self.db.query(Order).filter(Order.id == order_id).first()
        product_obj =  self.db.query(Product).filter(Product.id == product_id).first()

        if not order_obj:
            raise ServiceException(f"The order_id {order_id} is not exist")      
        
        if not product_obj:
            raise ServiceException(f"The product_id {product_id} is not exist")
 
        if  not order_obj.status == OrderStatus.PENDING.value:
            raise ServiceException(f"Can not to remove product from basket when order with status {order_obj.status} ")

        order_item_obj = self.db.query(OrderItem).filter(OrderItem.product_id == product_id and OrderItem.order_id == order_id).first()
        if count > order_item_obj.quantity:
            raise Exception("The product count that you want to remove from basket is more than of quantity of product in basket")
        if count < order_item_obj.quantity:
            order_obj.quantity -= count
            self.db.commit()
        if count == order_item_obj.quantity:
            self.db.delete(order_obj)
            self.db.commit()

