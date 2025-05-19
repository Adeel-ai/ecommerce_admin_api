from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category: str
    brand: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

class InventoryBase(BaseModel):
    product_id: int
    quantity: int

class InventoryUpdate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    last_updated: datetime
    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    product_id: int
    quantity: int
    total_price: float
    sold_at: datetime

class Sale(SaleBase):
    id: int
    class Config:
        orm_mode = True

class SalesSummary(BaseModel):
    total_revenue: Optional[float]
    total_sales: Optional[int]