from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.core.models.models import *
from src.core.schemas import schemas
from datetime import datetime, timedelta
from sqlalchemy import func
from typing import Optional

def create_product(db: Session, product: schemas.ProductCreate):
    try:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise ValueError("Product creation  failed")

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def get_inventory(db: Session):
    return db.query(Inventory).join(
        Product, Inventory.product_id == Product.id
    ).all()

def get_low_stock(db: Session, threshold: int = 10):
    return db.query(Inventory).filter(
        Inventory.quantity < threshold
    ).all()

def update_inventory(db: Session, inventory: schemas.InventoryUpdate):
    try:
        record = db.query(Inventory).filter(
            Inventory.product_id == inventory.product_id
        ).first()
        
        if not record:
            record = Inventory(
                product_id=inventory.product_id,
                quantity=inventory.quantity,
                last_updated=datetime.utcnow()
            )
            db.add(record)
        else:
            record.quantity = inventory.quantity
            record.last_updated = datetime.utcnow()
        
        db.commit()
        db.refresh(record)
        return record
    
    except Exception as e:
        db.rollback()
        raise Exception("Inventory update failed")

def get_sales(db: Session, start: datetime, end: datetime):
    end = end + timedelta(days=1)
    return db.query(Sale).filter(
        Sale.sold_at.between(start, end)
    ).order_by(Sale.sold_at.desc()).all()

def get_sales_summary(db: Session):
    try:
        result = db.query(
            func.sum(Sale.total_price).label("total_revenue"),
            func.count(Sale.id).label("total_sales")
        ).first()
        
        if not result or result.total_revenue is None:
            return {
                "total_revenue": 0.0,
                "total_sales": 0
            }
        
        return {
            "total_revenue": float(result.total_revenue),
            "total_sales": result.total_sales
        }
    except Exception as e:
        raise e

def get_sales_by_product(db: Session, product_id: int):
    return db.query(Sale).filter(Sale.product_id == product_id).all()

def get_sales_by_category(db: Session, category: str):
    return db.query(Sale).join(Product).filter(Product.category == category).all()

def get_revenue_by_period(db: Session, period: str):
    if period == "daily":
        time_format = func.date(Sale.sold_at)
    elif period == "weekly":
        time_format = func.date_format(Sale.sold_at, "%Y-%u")
    elif period == "monthly":
        time_format = func.date_format(Sale.sold_at, "%Y-%m")
    elif period == "annual":
        time_format = func.year(Sale.sold_at)
    else:
        raise ValueError("Invalid period")

    results = (
        db.query(
            time_format.label("period"),
            func.sum(Sale.total_price).label("revenue")
        )
        .group_by("period")
        .order_by("period")
        .all()
    )
    return [{"period": str(r[0]), "revenue": float(r[1])} for r in results]

def compare_revenue_periods(
    db: Session,
    period1_start: datetime,
    period1_end: datetime,
    period2_start: datetime,
    period2_end: datetime,
    category: Optional[str] = None
):
    q1 = db.query(func.sum(Sale.total_price)).join(Product).filter(
        Sale.sold_at >= period1_start,
        Sale.sold_at <= period1_end
    )
    q2 = db.query(func.sum(Sale.total_price)).join(Product).filter(
        Sale.sold_at >= period2_start,
        Sale.sold_at <= period2_end
    )

    if category:
        q1 = q1.filter(Product.category == category)
        q2 = q2.filter(Product.category == category)

    return {
        "period_1": {"start": period1_start, "end": period1_end, "revenue": q1.scalar() or 0},
        "period_2": {"start": period2_start, "end": period2_end, "revenue": q2.scalar() or 0}
    }