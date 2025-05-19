from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.schemas import schemas
from src.crud import crud
from src.core.db.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session=Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/", response_model=list[schemas.Product])
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)