from typing import List
from uuid import UUID,uuid4
from fastapi import FastAPI
from fastapi import HTTPException
from demo_entities import pType, Role, Product
import uvicorn as uv

app = FastAPI()

db: List[Product] = [
 Product(
 productId=uuid4(),
 productName="Car",
 productPrice=1000000,
 productType=pType.retail,
 roles=[Role.user],
 ),
 Product(
 productId=uuid4(),
 productName="Bus",
 productPrice=1000000,
 productType=pType.retail,
 roles=[Role.user],
 ),
 Product(
 productId=uuid4(),
 productName="Bike",
 productPrice=1000000,
 productType=pType.retail,
 roles=[Role.user],
 ),
 ]

#get employees
@app.get("/api/v1/products")
async def get_products():
    return db

# add new employee
@app.post("/api/v1/products")
async def create_products(products: Product):
 db.append(products)
 return {"id": products.productId}

#delete an employee
@app.delete("/api/v1/products/{id}")
async def delete_products(id: UUID):
    flag=False
    for product in db:
        if product.productId == id:
            db.remove(product)
            flag=True

    if flag==False: 
        raise HTTPException(
    status_code=404, detail=f"Delete employee failed, id {id} not found."
    )

    return

if __name__ == "__main__":
    uv.run("demo_main:app", host="0.0.0.0", port=8000 ,reload=True)