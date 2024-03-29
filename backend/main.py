from fastapi import FastAPI
from routers.product_router import router as product_router

app = FastAPI()

app.include_router(product_router)

@app.get("/health")
def health_check():
    return{"status":"ok"}