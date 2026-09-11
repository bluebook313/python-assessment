from sqlalchemy import select
from models import Product
from sqlalchemy.orm import Session

class ProductService:

    def __init__(self, db: Session):
        self.db = db

    async def add_item(self, name: str, price: int, count:int):
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
        product =  self.db.get(Product, product_id)
        return {
                    "Id":product.id, 
                    "Name":product.name, 
                    "Price":product.price, 
                    "Count":product.count
            } 