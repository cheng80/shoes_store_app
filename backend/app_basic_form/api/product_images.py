"""
ProductImage API - 제품 이미지 CRUD (Form 방식)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class ProductImage(BaseModel):
    id: Optional[int] = None
    pbid: Optional[int] = None
    imagePath: str


# ============================================
# 전체 제품 이미지 조회
# ============================================
@router.get("")
async def select_product_images():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pbid, imagePath 
            FROM ProductImage 
            ORDER BY id
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'pbid': row[1],
            'imagePath': row[2]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase ID로 이미지 조회
# ============================================
@router.get("/by_pbid/{pbid}")
async def select_product_images_by_pbid(pbid: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pbid, imagePath 
            FROM ProductImage 
            WHERE pbid = %s
            ORDER BY id
        """, (pbid,))
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'pbid': row[1],
            'imagePath': row[2]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 제품 이미지 조회
# ============================================
@router.get("/{image_id}")
async def select_product_image(image_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pbid, imagePath 
            FROM ProductImage 
            WHERE id = %s
        """, (image_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "ProductImage not found"}
        result = {
            'id': row[0],
            'pbid': row[1],
            'imagePath': row[2]
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품 이미지 추가
# ============================================
@router.post("")
async def insert_product_image(
    pbid: int = Form(...),
    imagePath: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "INSERT INTO ProductImage (pbid, imagePath) VALUES (%s, %s)"
        curs.execute(sql, (pbid, imagePath))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품 이미지 수정
# ============================================
@router.post("/{image_id}")
async def update_product_image(
    image_id: int,
    pbid: int = Form(...),
    imagePath: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "UPDATE ProductImage SET pbid=%s, imagePath=%s WHERE id=%s"
        curs.execute(sql, (pbid, imagePath, image_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품 이미지 삭제
# ============================================
@router.delete("/{image_id}")
async def delete_product_image(image_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM ProductImage WHERE id=%s"
        curs.execute(sql, (image_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.product_images (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="ProductImage API Test")
    test_app.include_router(router, prefix="/api/product_images")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

