from fastapi import FastAPI
from src.api import sales, inventory, products

app = FastAPI()

app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(products.router, prefix="/products", tags=["Products"])


@app.get("/")
async def root_hello():
    return {"message": "Hello world"}