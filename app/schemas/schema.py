from pydantic import BaseModel, ConfigDict, Field

class ProductStructure(BaseModel):
    name: str
    price: float
    product_count: int

