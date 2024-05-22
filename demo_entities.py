from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum
from pydantic import BaseModel

class pType(str, Enum):
 cosmetics = "cosmetics"
 retail = "retail"

class Role(str, Enum):
 admin = "admin"
 user = "user"

class Product(BaseModel):
 productId: Optional[UUID] = uuid4()
 productName: str
 productPrice: int
 productType: pType
 roles: List[Role]