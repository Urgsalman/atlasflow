from fastapi import FastAPI, HTTPException
from schemas import Product, StockUpdate

app = FastAPI(title="Inventory Service")

# Fausse base de données en mémoire pour l'instant
FAKE_DB = {
    "prod_1": {"id": "prod_1", "name": "Laptop", "stock": 5},
    "prod_2": {"id": "prod_2", "name": "Mouse", "stock": 0}
}

@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    product = FAKE_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.patch("/api/products/{product_id}/stock")
async def update_stock(product_id: str, update: StockUpdate):
    product = FAKE_DB.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product["stock"] < update.quantity_to_deduct:
        raise HTTPException(status_code=400, detail="Insufficient stock")
        
    product["stock"] -= update.quantity_to_deduct
    return {"message": "Stock updated", "new_stock": product["stock"]}