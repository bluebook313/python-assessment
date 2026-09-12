from pydantic import BaseModel, ConfigDict, Field

class ProductStructure(BaseModel):
    name: str
    price: float
    product_count: int


class OrderItemStructure(BaseModel):
    order_id : int
    product_count :int
    product_id : int

