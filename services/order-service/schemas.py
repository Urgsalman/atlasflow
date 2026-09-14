from pydantic import BaseModel, Field
from typing import List

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    customer_id: str
    items: List[OrderItem] = Field(..., min_length=1)