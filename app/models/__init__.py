from utils.database.connection import Base, engine
from schemas.config import OrderStatus
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)


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

    customer_id =  Column(
        ForeignKey("customers.id"),
        nullable=False,
    )
    status =  Column(
        String(30),
        default=OrderStatus.PENDING.value,
        nullable=False,
    )
    created_at =Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


