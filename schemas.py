"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    subtitle: Optional[str] = Field(None, description="Short marketing line")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    compare_at_price: Optional[float] = Field(None, ge=0, description="Original price for discount display")
    category: str = Field("Knee Massager", description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
    images: Optional[List[str]] = Field(default_factory=list, description="Image URLs")
    features: Optional[List[str]] = Field(default_factory=list, description="Bullet features")
    rating: Optional[float] = Field(4.8, ge=0, le=5, description="Average rating")
    reviews_count: Optional[int] = Field(0, ge=0, description="Number of reviews")

class OrderItem(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    title: str = Field(...)
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=1)

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    items: List[OrderItem]
    subtotal: float = Field(..., ge=0)
    shipping: float = Field(0, ge=0)
    total: float = Field(..., ge=0)

    customer_name: str = Field(...)
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    shipping_address: str = Field(...)
    city: str = Field(...)
    country: str = Field(...)
    postal_code: str = Field(...)
    notes: Optional[str] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
