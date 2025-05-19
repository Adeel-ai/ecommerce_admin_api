# E-commerce Admin API

Backend API service for managing product inventory and sales analytics.

## Overview

This service provides REST APIs for:
- Product management
- Inventory tracking with low-stock alerts
- Sales recording and analytics
- Revenue reporting with period comparisons

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+

### Installation

1. Clone the repository:
```
git clone https://github.com/Adeel-ai/ecommerce_admin_api.git
cd ecommerce_admin_api
```

2. Create and activate virtual environment:
```
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
```
cp .env.example .env
# Edit .env with your database credentials
```

5. Initialize the database:
```
alembic upgrade head
```

6. (Optional) Load demo data:
```
set PYTHONPATH=. # Windows
python -m src.core.db.init_demo_data
```

### Running the Service

```
uvicorn src.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development Notes

### Database Migrations

Generate new migration:
```
alembic revision --autogenerate -m "description"
```

Apply migrations:
```
alembic upgrade head
```

Rollback one version:
```
alembic downgrade -1
```

## Endpoint Details

### Product Endpoints (/products):

- POST /: Create a new product
- GET /: List all products (with pagination)

### Inventory Endpoints (/inventory):

- GET /status: Get current inventory levels for all products
- GET /low-stock: Get products with stock below threshold (default 10 units)
- PUT /update: Update inventory level for a specific product

### Sales Endpoints (/sales):

- GET /summary: Get overall sales metrics
- GET /range: Get sales records within a date range
- GET /by-product: Get sales for a specific product
- GET /by-category: Get sales for a specific category
- GET /revenue-by-period: Get revenue breakdown by time period (daily/weekly/monthly/annual)
- GET /compare-periods: Compare revenue between two time periods