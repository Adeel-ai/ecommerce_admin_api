from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.core.schemas import schemas
from src.crud import crud
from typing import Optional, List
from src.core.db.database import get_db

router = APIRouter()

@router.get("/summary", response_model=schemas.SalesSummary)
async def sales_summary(db: Session = Depends(get_db)):
    try:
        return crud.get_sales_summary(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate sales summary. Please try again later."
        )

@router.get("/range", response_model=List[schemas.Sale])
async def get_sales_range(
    start: datetime = Query(..., description="Start date (YYYY-MM-DD)"),
    end: datetime = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    if end < start:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date"
        )
    
    if (end - start).days > 90:
        raise HTTPException(
            status_code=400,
            detail="Date range cannot exceed 90 days"
        )
    
    try:
        return crud.get_sales(db, start, end)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve sales data"
        )

@router.get("/by-product")
def get_sales_by_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_sales_by_product(db, product_id)

@router.get("/by-category")
def get_sales_by_category(category: str, db: Session = Depends(get_db)):
    return crud.get_sales_by_category(db, category)

@router.get("/revenue/summary")
def get_revenue_summary(period: str = Query("daily", enum=["daily", "weekly", "monthly", "annual"]), db: Session = Depends(get_db)):
    return crud.get_revenue_by_period(db, period)

@router.get("/revenue/compare")
def compare_revenue(
    period1_start: datetime,
    period1_end: datetime,
    period2_start: datetime,
    period2_end: datetime,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.compare_revenue_periods(db, period1_start, period1_end, period2_start, period2_end, category)
