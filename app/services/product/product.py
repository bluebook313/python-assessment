from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Product
from utils.exceptions import ServiceException


class ProductService:

    def __init__(self, db: Session):
        self.db = db

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
            product = Product(
                name=name,
                price=price,
                count=count,
            )

            self.db.add(product)
            self.db.commit()
  

            return True

        except Exception as e:
            self.db.rollback()

            raise ServiceException(
                f"Could not create product: {e}"
            )

    # ==================================================
    # Get All
    # ==================================================

    async def get_all_item(self):

        try:
            products = self.db.scalars(
                select(Product)
            ).all()

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
            product = self.db.get(
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
