from sqlalchemy import select
from models import Product
from sqlalchemy.orm import Session
from utils.exceptions import *

class ProductService:

    def __init__(self, db: Session):
        self.db = db

    async def add_item(self, name: str, price: int, count:int):
        if len(name)>200:
            raise ServiceException("The product name is too long !")
        if price<=0 or count<=0:
            raise ValueError("The price or product count must  bigger than 0 ")
        product = Product(
            name=name,
            price=price,
            count=count
        )

        self.db.add(product)
        self.db.commit()

        return product
    
    
    async def get_all_item(self):
        product_list =  self.db.scalars(
            select(Product)
        ).all()
        return {pr.id:{"Name":pr.name, "Price":pr.price, "Count":pr.count} for pr in product_list}
            
        

    async def get_item(self, product_id: int):
        if product_id<=0 :
            raise ValueError("The product_id  must bigger than 0 ")
        product =  self.db.get(Product, product_id)
        if not product:
            raise ServiceException(f"The product with id {product_id} is not exist")
        return {
                    "Id":product.id, 
                    "Name":product.name, 
                    "Price":product.price, 
                    "Count":product.count
            } 