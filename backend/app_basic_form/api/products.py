"""
Product API - 제품 CRUD (Form 방식)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class Product(BaseModel):
    id: Optional[int] = None
    pbid: Optional[int] = None
    mfid: Optional[int] = None
    size: int
    basePrice: int
    pQuantity: int


# ============================================
# 전체 제품 조회
# ============================================
@router.get("")
async def select_products():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pbid, mfid, size, basePrice, pQuantity 
            FROM Product 
            ORDER BY id
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase ID로 제품 조회
# ============================================
@router.get("/by_pbid/{pbid}")
async def select_products_by_pbid(pbid: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pbid, mfid, size, basePrice, pQuantity 
            FROM Product 
            WHERE pbid = %s
            ORDER BY size
        """, (pbid,))
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 제품 조회
# ============================================
@router.get("/{product_id}")
async def select_product(product_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pbid, mfid, size, basePrice, pQuantity 
            FROM Product 
            WHERE id = %s
        """, (product_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "Product not found"}
        result = {
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5]
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품 추가
# ============================================
@router.post("")
async def insert_product(
    pbid: int = Form(...),
    mfid: int = Form(...),
    size: int = Form(...),
    basePrice: int = Form(...),
    pQuantity: int = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            INSERT INTO Product (pbid, mfid, size, basePrice, pQuantity) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (pbid, mfid, size, basePrice, pQuantity))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품 수정
# ============================================
@router.post("/{product_id}")
async def update_product(
    product_id: int,
    pbid: int = Form(...),
    mfid: int = Form(...),
    size: int = Form(...),
    basePrice: int = Form(...),
    pQuantity: int = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE Product 
            SET pbid=%s, mfid=%s, size=%s, basePrice=%s, pQuantity=%s 
            WHERE id=%s
        """
        curs.execute(sql, (pbid, mfid, size, basePrice, pQuantity, product_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제품 삭제
# ============================================
@router.delete("/{product_id}")
async def delete_product(product_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM Product WHERE id=%s"
        curs.execute(sql, (product_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.products (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Product API Test")
    test_app.include_router(router, prefix="/api/products")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

