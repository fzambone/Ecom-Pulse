
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from repositories.category_repository import CategoryRepository
from utils.database import get_db
from utils.auth import get_current_user


router = APIRouter()

@router.get("/categories", response_model=List[CategoryResponse])
def read_categories(skip: int = 0, 
                    limit: int = 100,
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    categories = CategoryRepository(db).get_all(skip, limit).all()
    return categories

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate,
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    return CategoryRepository(db).create(category)

@router.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int,
                  db: Session = Depends(get_db),
                  current_user: dict = Depends(get_current_user)):
    db_category = CategoryRepository(db).get(category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int,
                    category: CategoryUpdate,
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    db_category = CategoryRepository(db).get(category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    for var, value in vars(category).items():
        if value is not None:
            setattr(db_category, var, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int,
                    db: Session = Depends(get_db),
                    current_user: dict = Depends(get_current_user)):
    CategoryRepository(db).soft_delete(category_id)
    return {"ok": True}