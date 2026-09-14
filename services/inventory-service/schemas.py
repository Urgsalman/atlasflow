from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str
    name: str
    stock: int

class StockUpdate(BaseModel):
    quantity_to_deduct: int = Field(..., gt=0)