from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from utils.auth import get_current_user
from schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from repositories.product_repository import ProductRepository
from utils.database import get_db

router = APIRouter()

@router.get("/products", response_model=List[ProductResponse])
def read_products(skip: int = 0, 
                  limit: int = 100, 
                  db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)
                  ):
    products = ProductRepository(db).get_all(skip, limit).all()
    return products

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, 
                   db: Session = Depends(get_db),
                   current_user: dict = Depends(get_current_user)
                   ):
    return ProductRepository(db).create(product)

@router.get("/product/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, 
                 db: Session = Depends(get_db),
                 current_user: dict = Depends(get_current_user)
                 ):
    db_product = ProductRepository(db).get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, 
                   product: ProductUpdate, 
                   db: Session = Depends(get_db),
                   current_user: dict = Depends(get_current_user)
                   ):
    db_product = ProductRepository(db).get(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for var, value in vars(product).items():
        if value is not None:
            setattr(db_product, var, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int,
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    ProductRepository(db).soft_delete(product_id)
    return {"ok": True}