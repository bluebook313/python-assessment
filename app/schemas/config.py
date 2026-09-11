from enum import Enum

class OrderStatus(str, Enum):
    PENDING     = "pending"
    PAID        = "paid"
    PROCESSING  = "processing"
    COMPLETED   = "completed"
    CANCELLED   = "cancelled"


class TaskEnum(str, Enum):
    pass


DATABASE_URL = "sqlite:///./orders.db"