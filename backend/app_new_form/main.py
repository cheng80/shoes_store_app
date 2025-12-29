"""
FastAPI 메인 애플리케이션 - 새로운 ERD 구조
모든 모델의 CRUD API 제공 (Form 데이터 방식)
"""

from fastapi import FastAPI
from app_new_form.database.connection import connect_db

# 기본 라우터 import
from app_new_form.api import branch
from app_new_form.api import users
from app_new_form.api import staff
from app_new_form.api import maker
from app_new_form.api import kind_category
from app_new_form.api import color_category
from app_new_form.api import size_category
from app_new_form.api import gender_category
from app_new_form.api import product
from app_new_form.api import purchase_item
from app_new_form.api import pickup
from app_new_form.api import refund
from app_new_form.api import receive
from app_new_form.api import request

# JOIN 라우터 import
from app_new_form.api import product_join
from app_new_form.api import purchase_item_join
from app_new_form.api import pickup_join
from app_new_form.api import refund_join
from app_new_form.api import receive_join
from app_new_form.api import request_join

app = FastAPI(title="Shoes Store API - 새로운 ERD 구조")
ip_address = '127.0.0.1'

# 기본 CRUD 라우터 등록
app.include_router(branch.router, prefix="/api/branches", tags=["branches"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(staff.router, prefix="/api/staffs", tags=["staffs"])
app.include_router(maker.router, prefix="/api/makers", tags=["makers"])
app.include_router(kind_category.router, prefix="/api/kind_categories", tags=["kind_categories"])
app.include_router(color_category.router, prefix="/api/color_categories", tags=["color_categories"])
app.include_router(size_category.router, prefix="/api/size_categories", tags=["size_categories"])
app.include_router(gender_category.router, prefix="/api/gender_categories", tags=["gender_categories"])
app.include_router(product.router, prefix="/api/products", tags=["products"])
app.include_router(purchase_item.router, prefix="/api/purchase_items", tags=["purchase_items"])
app.include_router(pickup.router, prefix="/api/pickups", tags=["pickups"])
app.include_router(refund.router, prefix="/api/refunds", tags=["refunds"])
app.include_router(receive.router, prefix="/api/receives", tags=["receives"])
app.include_router(request.router, prefix="/api/requests", tags=["requests"])

# JOIN 라우터 등록
app.include_router(product_join.router, prefix="/api/products", tags=["products-join"])
app.include_router(purchase_item_join.router, prefix="/api/purchase_items", tags=["purchase_items-join"])
app.include_router(pickup_join.router, prefix="/api/pickups", tags=["pickups-join"])
app.include_router(refund_join.router, prefix="/api/refunds", tags=["refunds-join"])
app.include_router(receive_join.router, prefix="/api/receives", tags=["receives-join"])
app.include_router(request_join.router, prefix="/api/requests", tags=["requests-join"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Shoes Store API - 새로운 ERD 구조",
        "status": "running",
        "endpoints": {
            "branches": "/api/branches",
            "users": "/api/users",
            "staffs": "/api/staffs",
            "makers": "/api/makers",
            "kind_categories": "/api/kind_categories",
            "color_categories": "/api/color_categories",
            "size_categories": "/api/size_categories",
            "gender_categories": "/api/gender_categories",
            "products": "/api/products",
            "purchase_items": "/api/purchase_items",
            "pickups": "/api/pickups",
            "refunds": "/api/refunds",
            "receives": "/api/receives",
            "requests": "/api/requests"
        },
        "join_endpoints": {
            "products_join": "/api/products/{id}/full_detail, /api/products/with_categories",
            "purchase_items_join": "/api/purchase_items/{id}/with_details, /api/purchase_items/{id}/full_detail",
            "pickups_join": "/api/pickups/{id}/with_details, /api/pickups/{id}/full_detail",
            "refunds_join": "/api/refunds/{id}/with_details, /api/refunds/{id}/full_detail",
            "receives_join": "/api/receives/{id}/with_details, /api/receives/{id}/full_detail",
            "requests_join": "/api/requests/{id}/with_details, /api/requests/{id}/full_detail"
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

