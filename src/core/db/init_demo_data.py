from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from src.core.db.database import SessionLocal
from src.core.models.models import Product, Sale, Inventory

def seed_demo_data():
    db: Session = SessionLocal()

    db.query(Sale).delete()
    db.query(Inventory).delete()
    db.query(Product).delete()
    db.commit()
    
    product_names = [
        ("iPhone 15", "Electronics", "Apple"),
        ("Galaxy S23", "Electronics", "Samsung"),
        ("MacBook Pro", "Computers", "Apple"),
        ("Dell XPS 15", "Computers", "Dell"),
        ("Sony WH-1000XM5", "Audio", "Sony"),
        ("Kindle Paperwhite", "Books", "Amazon"),
        ("Instant Pot", "Kitchen", "Instant"),
        ("Echo Dot", "Smart Home", "Amazon")
    ]

    products = []
    for name, category,brand in product_names:
        product = Product(
            name=name,
            category=category,
            brand=brand,
            price=round(random.uniform(50, 2000), 2)
        )
        db.add(product)
        products.append(product)

    db.commit()

    for product in products:
        db.refresh(product)

    for product in products:
        for _ in range(random.randint(5, 15)):
            days_ago = random.randint(1, 30)
            sale_date = datetime.utcnow() -timedelta(days=days_ago)
            quantity = random.randint(1, 5)
            total_price = round(product.price * quantity, 2)

            sale = Sale(
                product_id=product.id,
                quantity=quantity,
                total_price=total_price,
                sold_at=sale_date
            )
            db.add(sale)

    db.commit()
    print("Demo data inserted.")

if __name__ == "__main__":
    seed_demo_data()
