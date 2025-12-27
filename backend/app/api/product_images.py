"""
ProductImage API
RESTful 기본 CRUD
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.all_models import ProductImage
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_product_images(
    pbid: Optional[int] = Query(None, description="ProductBase ID로 필터"),
    order_by: str = Query("id", description="정렬 기준"),
    order: str = Query("asc", description="정렬 방향 (asc, desc)")
):
    """제품 이미지 조회 (필터링 및 정렬 가능)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        conditions = []
        params = []
        
        if pbid is not None:
            conditions.append("pbid = %s")
            params.append(pbid)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        
        sql = f"""
        SELECT id, pbid, imagePath 
        FROM ProductImage 
        WHERE {where_clause} 
        ORDER BY {order_by} {order_direction}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pbid': row[1],
                'imagePath': row[2]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{image_id}")
async def get_product_image(image_id: int):
    """ID로 제품 이미지 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, pbid, imagePath FROM ProductImage WHERE id = %s"
        curs.execute(sql, (image_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'ProductImage not found'}
        
        result = {
            'id': row[0],
            'pbid': row[1],
            'imagePath': row[2]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_product_image(product_image: ProductImage):
    """제품 이미지 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        if product_image.pbid is None:
            return {"result": "Error", "message": "pbid is required"}
        
        sql = "INSERT INTO ProductImage (pbid, imagePath) VALUES (%s, %s)"
        curs.execute(sql, (product_image.pbid, product_image.imagePath))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{image_id}")
async def update_product_image(image_id: int, product_image: ProductImage):
    """제품 이미지 수정"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "UPDATE ProductImage SET pbid=%s, imagePath=%s WHERE id=%s"
        curs.execute(sql, (product_image.pbid, product_image.imagePath, image_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{image_id}")
async def delete_product_image(image_id: int):
    """제품 이미지 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM ProductImage WHERE id=%s"
        curs.execute(sql, (image_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app.api.product_images (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="ProductImage API Test")
    test_app.include_router(router, prefix="/api/product_images")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)
