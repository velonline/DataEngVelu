from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum
import random
from Product import Product, Inventory, Order,Shipment, ProductType

app = FastAPI()


products : List[Product] = []
inventory: List[Inventory] = []
orders: List[Order] = []
shipments: List[Shipment] = []


def initializeInventory():
    for i in range(20):
        product = Product(id=uuid4(), name=f"Product {i}", price=random.randrange(10, 500), product_type=ProductType.storage)
        products.append(product)
        # Toss a coin to decide if the product is in stock
        if random.choice([True, False]):
            quantity = random.randrange(1, 100)
            inventory.append(Inventory(product=product, quantity=quantity))

@app.get("/products", response_model=List[Product])
async def get_products():
    return products

@app.post("/products", response_model=Product, status_code=201)
async def create_product(product: Product):
    products.append(product)
    return product

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: UUID):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: UUID, product: Product):
    for i, p in enumerate(products):
        if p.id == product_id:
            products[i] = product
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: UUID):
    for i, product in enumerate(products):
        if product.id == product_id:
            del products[i]
            return
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/inventory", response_model=List[Inventory])
async def get_inventory():
    return inventory

@app.post("/inventory", response_model=Inventory, status_code=201)
async def create_inventory(inventory_item: Inventory):
    for product in products:
        if product.id == inventory_item.product.id:
            inventory.append(inventory_item)
            return inventory_item
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/inventory/{product_id}", response_model=Inventory)
async def get_inventory_item(product_id: UUID):
    for item in inventory:
        if item.product.id == product_id:
            return item
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/inventory/{product_id}", response_model=Inventory)
async def update_inventory(product_id: UUID, inventory_item: Inventory):
    for i, item in enumerate(inventory):
        if item.product.id == product_id:
            inventory[i] = inventory_item
            return inventory_item
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/inventory/{product_id}")
async def delete_inventory(product_id: UUID):
    for i, item in enumerate(inventory):
        if item.product.id == product_id:
            del inventory[i]
            return
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/orders", response_model=List[Order])
async def get_orders():
    return orders

@app.post("/orders", response_model=Order, status_code=201)
async def create_order(order: Order):
    for item in order.products:
        if item.product.id not in [product.id for product in products]:
            raise HTTPException(status_code=404, detail=f"Product {item.product.id} not found")
        if item.product.id not in [item.product.id for item in inventory]:
            raise HTTPException(status_code=404, detail=f"Product {item.product.id} not in stock")
        selected_inventory_item = None
        for i, inventory_item in enumerate(inventory):
            if item.product.id == inventory_item.product.id:
                selected_inventory_item = inventory_item
        if inventory_item.quantity < item.quantity:
            raise HTTPException(status_code=404, detail=f"Not enough stock for item {item.product.id}")
        selected_inventory_item.quantity -= item.quantity
        inventory[i] = selected_inventory_item
    orders.append(order)
    shipments.append(Shipment(id=uuid4(), order=order, status="Pending"))
    return order

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: UUID):
    for order in orders:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}/{status}", response_model=Order)
async def update_order(order_id: UUID, status: str):
    for i, order in enumerate(orders):
        if order.id == order_id:
            orders[i].status = status
            return orders[i]
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}")
async def delete_order(order_id: UUID):
    for i, order in enumerate(orders):
        if order.id == order_id:
            del orders[i]
            return
    raise HTTPException(status_code=404, detail="Order not found")

@app.get("/shipments", response_model=List[Shipment])
async def get_shipments():
    return shipments

@app.get("/shipments/{shipment_id}", response_model=Shipment)
async def get_shipment(shipment_id: UUID):
    for shipment in shipments:
        if shipment.id == shipment_id:
            return shipment
    raise HTTPException(status_code=404, detail="Shipment not found")

@app.put("/shipments/{shipment_id}/{status}", response_model=Shipment)
async def update_shipment(shipment_id: UUID, status: str):
    for i, shipment in enumerate(shipments):
        if shipment.id == shipment_id:
            shipments[i].status = status
            if status == "shipped":
                for i, order in enumerate(orders):
                    if order.id == shipment.order.id:
                        orders[i].status = "shipped"
            elif status == "delivered":
                for i, order in enumerate(orders):
                    if order.id == shipment.order.id:
                        orders[i].status = "delivered"
            return shipments[i]
    raise HTTPException(status_code=404, detail="Shipment not found")

initializeInventory()
# Main point to run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

