"""
Product API - 제품 CRUD
개별 실행: python products.py
"""

from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Optional
from database.connection import connect_db

app = FastAPI()
ipAddress = "127.0.0.1"


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
@app.get("/select_products")
async def select_products():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pbid, mfid, size, basePrice, pQuantity 
        FROM Product 
        ORDER BY id
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'pbid': row[1],
        'mfid': row[2],
        'size': row[3],
        'basePrice': row[4],
        'pQuantity': row[5]
    } for row in rows]
    return {"results": result}


# ============================================
# ProductBase ID로 제품 조회
# ============================================
@app.get("/select_products_by_pbid/{pbid}")
async def select_products_by_pbid(pbid: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pbid, mfid, size, basePrice, pQuantity 
        FROM Product 
        WHERE pbid = %s
        ORDER BY size
    """, (pbid,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'pbid': row[1],
        'mfid': row[2],
        'size': row[3],
        'basePrice': row[4],
        'pQuantity': row[5]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 제품 조회
# ============================================
@app.get("/select_product/{product_id}")
async def select_product(product_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pbid, mfid, size, basePrice, pQuantity 
        FROM Product 
        WHERE id = %s
    """, (product_id,))
    row = curs.fetchone()
    conn.close()
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


# ============================================
# 제품 추가
# ============================================
@app.post("/insert_product")
async def insert_product(
    pbid: int = Form(...),
    mfid: int = Form(...),
    size: int = Form(...),
    basePrice: int = Form(...),
    pQuantity: int = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO Product (pbid, mfid, size, basePrice, pQuantity) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (pbid, mfid, size, basePrice, pQuantity))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제품 수정
# ============================================
@app.post("/update_product")
async def update_product(
    product_id: int = Form(...),
    pbid: int = Form(...),
    mfid: int = Form(...),
    size: int = Form(...),
    basePrice: int = Form(...),
    pQuantity: int = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE Product 
            SET pbid=%s, mfid=%s, size=%s, basePrice=%s, pQuantity=%s 
            WHERE id=%s
        """
        curs.execute(sql, (pbid, mfid, size, basePrice, pQuantity, product_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제품 삭제
# ============================================
@app.delete("/delete_product/{product_id}")
async def delete_product(product_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM Product WHERE id=%s"
        curs.execute(sql, (product_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

