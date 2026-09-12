from models import Customer
from sqlalchemy.orm import Session
from utils.exceptions import ServiceException


class CustomerService:

    def __init__(self, db: Session):
        self.db = db

    async def get_customer_info(self, customer_id):
        """
        return customer info
        """
        if customer_id <= 0:
            raise ServiceException("The customer_id must  bigger than 0 ")
        if not isinstance(customer_id, int):
            raise ServiceException("The customer_id must  integer ")
        
        customer_obj = self.db.query(Customer).where(Customer.id == customer_id).first()
        if not customer_obj:
            raise ServiceException(f"The customer_id {customer_id} is not exist")
        return {
            "Id":customer_id,
            "name":customer_obj.name,
            "email":customer_obj.email,
        }
    


    async def add_customer(self, name, email):
        """
        add new customer to database
        """
        customer_obj = self.db.query(Customer).where(Customer.email == email).first()
        if customer_obj:
            raise ServiceException(f"The user with the email {email} exist.")
        new_customer = Customer(
            name=name,
            email=email,
        )
        self.db.add(new_customer)
        self.db.commit()
        return True

