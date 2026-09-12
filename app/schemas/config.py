from enum import Enum
from pathlib import Path
import logging
import os

class OrderStatus(str, Enum):
    PENDING     = "pending"
    PAID        = "paid"
    PROCESSING  = "processing"
    COMPLETED   = "completed"
    CANCELLED   = "cancelled"
    FAILED      =  "FAILED"


class TaskEnum(str, Enum):
    pass

DATABASE_URL = "sqlite:///orders.db"  
ProjectBaseFolder = Path(__file__).resolve().parent.resolve().parent


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(ProjectBaseFolder,"app.log")),
    ],
)

log = logging.getLogger()
 