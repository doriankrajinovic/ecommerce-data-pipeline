
"""Pydantic modeli za e-commerce podatke. 
Definiraju strukturu i validaciju podataka. 
"""

from datetime import datetime 
from decimal import Decimal 
from enum import Enum 
from typing import Optional 

from pydantic import BaseModel, Field, EmailStr, field_validator 



class OrderStatus(str, Enum):
    """Status narudžbe"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class ProductCategory(str, Enum):
    """Kategorija proizvoda"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    SPORTS = "sports"
    BOOKS = "books"



class Customer(BaseModel): 
    """Model kupca"""
    customer_id: str = Field(..., description="Jedinstveni ID kupca")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email : EmailStr
    country: str = Field(..., min_length=2, max_length=100)
    created_at: datetime 

    @field_validator('country')
    @classmethod
    def validate_country(cls, v: str) -> str: 
        """Očisti i formatiraj country"""
        return v.strip().title() 
    
class Order(BaseModel):
    """Model narudžbe."""
    order_id: str = Field(..., description="Unique order identifier")
    customer_id: str
    order_date: datetime
    status: OrderStatus
    total_amount: Decimal = Field(..., ge=0, decimal_places=2)


class Product(BaseModel):
    """Model proizvoda."""
    product_id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., min_length=1, max_length=200)
    category: ProductCategory
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock_quantity: int = Field(..., ge=0)
    created_at: datetime


class OrderItem(BaseModel):
    """Model stavke narudžbe"""
    order_item_id: str
    order_id: str
    product_id: str
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., gt=0, decimal_places=2)

    @property
    def line_total(self) -> Decimal:
        """Ukupna cijena stavke"""
        return self.quantity * self.unit_price 


if __name__ == "__main__":
    #test customer 

    customer = Customer (
        customer_id="CUST-001", 
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        country="US",
        created_at=datetime.now()
    )
    print(customer)
    
    #test order 
        
    
