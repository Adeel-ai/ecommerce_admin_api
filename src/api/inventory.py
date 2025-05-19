from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.schemas import schemas
from src.crud import crud
from src.core.db.database import get_db

router = APIRouter()

@router.get("/status", response_model=list[schemas.Inventory])
def get_inventory_status(db: Session = Depends(get_db)):
    try:
        return crud.get_inventory(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/low-stock", response_model=list[schemas.Inventory])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    try:
        return crud.get_low_stock(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update", response_model=schemas.Inventory)
def update_inventory(inventory: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_inventory(db, inventory)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))