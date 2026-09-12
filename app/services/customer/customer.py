from models import Customer
from sqlalchemy.orm import Session



class CustomerService:

    def __init__(self, db: Session):
        self.db = db

    async def get_customer_info(self, customer_id):
        """
        add product to basket
        """
        customer_obj = self.db.query(Customer).where(Customer.id == customer_id).first()
        return {
            "Id":customer_id,
            "name":customer_obj.name,
            "email":customer_obj.email,
        }
    


    async def add_customer(self, name, email):
        """
        add product to basket
        """
        new_customer = Customer(
            name=name,
            email=email,
        )
        self.db.add(new_customer)
        self.db.commit()
        return True

