from sqlalchemy import select, update
from sqlalchemy.orm import Session

from models import Product
from utils.exceptions import ServiceException


class ProductService:

    def __init__(self, db: Session):
        self.db  = db

    # ==================================================
    # Create
    # ==================================================

    async def add_item(
        self,
        name: str,
        price: int,
        count: int,
    ):
        if len(name) > 200:
            raise ServiceException(
                "The product name is too long!"
            )
        
        try:
            product_obj = await self.db.scalars(
                select(Product)
                .where(
                    Product.name == name,
                )
            )
            product_obj= product_obj.first()
             
            if product_obj:
                print(100*"=") 
                await self.db.execute(
                    update(Product)
                    .where(Product.id == product_obj.id)
                    .values(
                        # Ignore change the price 
                        count=Product.count + count
                    )
                )
                await self.db.commit()
                return {
                    "Id":product_obj.id
                }
            
            else:
                print(100*"-") 
                product = Product(
                    name=name,
                    price=price,
                    count=count,
                )

                self.db.add(product)
                await self.db.commit()
    

                return {
                    "Id":product.id
                }

        except Exception as e:
            await self.db.rollback()

            raise ServiceException(
                f"Could not create product: {e}"
            )

    # ==================================================
    # Get All
    # ==================================================

    async def get_all_item(self):

        try:
            result = await self.db.scalars(
                select(Product)
            )

            products = result.all()

            return {
                product.id: {
                    "Name": product.name,
                    "Price": product.price,
                    "Count": product.count,
                }
                for product in products
            }

        except Exception as e:

            raise ServiceException(
                f"Could not get products: {e}"
            )

    # ==================================================
    # Get One
    # ==================================================

    async def get_item(
        self,
        product_id: int,
    ):

        try:
            product = await self.db.get(
                Product,
                product_id,
            )

            if not product:
                raise ServiceException(
                    f"Product with id {product_id} "
                    f"does not exist"
                )

            return {
                "Id": product.id,
                "Name": product.name,
                "Price": product.price,
                "Count": product.count,
            }

        except ServiceException:
            raise

        except Exception as e:

            raise ServiceException(
                f"Could not get product: {e}"
            )
