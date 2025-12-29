"""
FastAPI 메인 애플리케이션 - Form 방식
모든 모델의 CRUD API 제공 (Form 데이터 방식)
"""

from fastapi import FastAPI
from app_basic_form.database.connection import connect_db

# 기본 라우터 import
from app_basic_form.api import customers
from app_basic_form.api import employees
from app_basic_form.api import manufacturers
from app_basic_form.api import product_bases
from app_basic_form.api import product_images
from app_basic_form.api import products
from app_basic_form.api import purchases
from app_basic_form.api import purchase_items
from app_basic_form.api import login_histories

# JOIN 라우터 import
from app_basic_form.api import products_join
from app_basic_form.api import purchases_join
from app_basic_form.api import product_bases_join
from app_basic_form.api import purchase_items_join

app = FastAPI(title="Shoes Store API - Form 방식")
ip_address = '127.0.0.1'

# 기본 CRUD 라우터 등록
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(employees.router, prefix="/api/employees", tags=["employees"])
app.include_router(manufacturers.router, prefix="/api/manufacturers", tags=["manufacturers"])
app.include_router(product_bases.router, prefix="/api/product_bases", tags=["product_bases"])
app.include_router(product_images.router, prefix="/api/product_images", tags=["product_images"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(purchases.router, prefix="/api/purchases", tags=["purchases"])
app.include_router(purchase_items.router, prefix="/api/purchase_items", tags=["purchase_items"])
app.include_router(login_histories.router, prefix="/api/login_histories", tags=["login_histories"])

# JOIN 라우터 등록
app.include_router(products_join.router, prefix="/api/products", tags=["products-join"])
app.include_router(purchases_join.router, prefix="/api/purchases", tags=["purchases-join"])
app.include_router(product_bases_join.router, prefix="/api/product_bases", tags=["product_bases-join"])
app.include_router(purchase_items_join.router, prefix="/api/purchase_items", tags=["purchase_items-join"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Shoes Store API - Form 방식",
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
        },
        "join_endpoints": {
            "products_join": "/api/products/{id}/with_base, /api/products/{id}/full_detail",
            "purchases_join": "/api/purchases/{id}/with_customer, /api/purchases/{id}/with_items",
            "product_bases_join": "/api/product_bases/with_first_image, /api/product_bases/full_detail",
            "purchase_items_join": "/api/purchase_items/{id}/full_detail, /api/purchase_items/by_pcid/{pcid}/full_detail"
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

