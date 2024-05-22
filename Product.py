from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum
import random

class ProductType(str, Enum):
    storage = "storage"
    networking = "networking"
    peripherals = "peripherals"
    cpu = "cpu"
    display = "display"
    battery = "battery"
 
class Product(BaseModel):
    id: UUID = uuid4()
    name: str
    price: float
    product_type: ProductType
 
class Inventory(BaseModel):
    product: Product
    quantity: int
 
class Order(BaseModel):
    id : UUID = uuid4()
    products: List[Inventory]
    status: str
 
class Shipment(BaseModel):
    id : UUID = uuid4()
    order: Order
    status: str
 