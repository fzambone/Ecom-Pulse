from fastapi import FastAPI
from routers.product_router import router as product_router
from routers.category_router import router as category_router

app = FastAPI()

app.include_router(product_router)
app.include_router(category_router)

@app.get("/health")
def health_check():
    return{"status":"ok"}