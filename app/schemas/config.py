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


DATABASE_URL = os.getenv("DATABASE_URL")
ServerIp=os.getenv("ServerIp")
ServerPort=os.getenv("ServerPort")
ReloadServer=os.getenv("ReloadServer")
if ReloadServer == 1:
    ReloadServer = True

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
 