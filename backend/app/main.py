"""
FastAPI 메인 애플리케이션
모든 모델의 CRUD API 제공
"""

from fastapi import FastAPI
from app.database.connection import connect_db

# 라우터 import
from app.api import customers
from app.api import employees
from app.api import manufacturers
from app.api import product_bases
from app.api import product_images
from app.api import products
from app.api import purchases
from app.api import purchase_items
from app.api import login_histories

app = FastAPI()
ip_address = '127.0.0.1'

# 모든 라우터 등록
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(manufacturers.router, prefix="/api/manufacturers", tags=["manufacturers"])
app.include_router(product_bases.router, prefix="/api/product_bases", tags=["product_bases"])
app.include_router(product_images.router, prefix="/api/product_images", tags=["product_images"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(purchases.router, prefix="/api/purchases", tags=["purchases"])
app.include_router(purchase_items.router, prefix="/api/purchase_items", tags=["purchase_items"])
app.include_router(login_histories.router, prefix="/api/login_histories", tags=["login_histories"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Shoes Store API",
        "status": "running",
        "endpoints": {
            "customers": "/api/customers",
            "employees": "/api/employees",
            "manufacturers": "/api/manufacturers",
            "product_bases": "/api/product_bases",
            "product_images": "/api/product_images",
            "products": "/api/products",
            "purchases": "/api/purchases",
            "purchase_items": "/api/purchase_items",
            "login_histories": "/api/login_histories"
        }
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    try:
        conn = connect_db()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ip_address, port=8000)

