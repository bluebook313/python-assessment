from utils.database.connection import engine
from schemas.config import OrderStatus
from sqlalchemy import (
    UniqueConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass   
class Product(Base):
    __tablename__ = "products"

    id =  Column(Integer, primary_key=True)
    name =  Column(String(200), nullable=False)
    price =  Column(Float, nullable=False)
    count =  Column(Integer, nullable=False, default=0)

class Customer(Base):
    __tablename__ = "customers"

    id =  Column(Integer, primary_key=True)
    name =  Column(String(200), nullable=False)
    email =  Column(String(255), nullable=False)

class Order(Base):
    __tablename__ = "orders"    
    
    id =  Column(Integer, primary_key=True)
    customer_id =  Column(ForeignKey("customers.id"), nullable=False,)
    total_price =  Column(Float, nullable=True)
    status =Column(String(30), default=OrderStatus.PENDING.value, nullable=False,)
    created_at =Column(DateTime, nullable=False,)

 
class OrderItem(Base):
    __tablename__ = "order_items"

    id =  Column(Integer, primary_key=True)
    order_id =  Column(ForeignKey("orders.id"), nullable=False)
    product_id =  Column(ForeignKey("products.id"), nullable=False)    
    quantity =  Column(Integer, nullable=False)
    total_order_price =  Column(Float, nullable=False)
    
    __table_args__ = (
        UniqueConstraint("order_id", "product_id"),
    )
    
# Base.metadata.create_all(engine) #Remove this line when use alembic as database manager