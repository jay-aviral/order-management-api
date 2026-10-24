from fastapi import FastAPI

from app.routers import auth, orders, products

app = FastAPI(title="Order Management API", version="1.0.0")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}