"""
Product API - 제품 CRUD
개별 실행: python product.py
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
    p_seq: Optional[int] = None
    kc_seq: int
    cc_seq: int
    sc_seq: int
    gc_seq: int
    m_seq: int
    p_name: Optional[str] = None
    p_price: int = 0
    p_stock: int = 0
    p_image: Optional[str] = None


# ============================================
# 전체 제품 조회
# ============================================
@app.get("/select_products")
async def select_products():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT p_seq, kc_seq, cc_seq, sc_seq, gc_seq, m_seq, p_name, p_price, p_stock, p_image 
        FROM product 
        ORDER BY p_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'p_seq': row[0],
        'kc_seq': row[1],
        'cc_seq': row[2],
        'sc_seq': row[3],
        'gc_seq': row[4],
        'm_seq': row[5],
        'p_name': row[6],
        'p_price': row[7],
        'p_stock': row[8],
        'p_image': row[9]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 제품 조회
# ============================================
@app.get("/select_product/{product_seq}")
async def select_product(product_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT p_seq, kc_seq, cc_seq, sc_seq, gc_seq, m_seq, p_name, p_price, p_stock, p_image 
        FROM product 
        WHERE p_seq = %s
    """, (product_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Product not found"}
    result = {
        'p_seq': row[0],
        'kc_seq': row[1],
        'cc_seq': row[2],
        'sc_seq': row[3],
        'gc_seq': row[4],
        'm_seq': row[5],
        'p_name': row[6],
        'p_price': row[7],
        'p_stock': row[8],
        'p_image': row[9]
    }
    return {"result": result}


# ============================================
# 제조사별 제품 조회
# ============================================
@app.get("/select_products_by_maker/{maker_seq}")
async def select_products_by_maker(maker_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT p_seq, kc_seq, cc_seq, sc_seq, gc_seq, m_seq, p_name, p_price, p_stock, p_image 
        FROM product 
        WHERE m_seq = %s
        ORDER BY p_seq
    """, (maker_seq,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'p_seq': row[0],
        'kc_seq': row[1],
        'cc_seq': row[2],
        'sc_seq': row[3],
        'gc_seq': row[4],
        'm_seq': row[5],
        'p_name': row[6],
        'p_price': row[7],
        'p_stock': row[8],
        'p_image': row[9]
    } for row in rows]
    return {"results": result}


# ============================================
# 제품 추가
# ============================================
@app.post("/insert_product")
async def insert_product(
    kc_seq: int = Form(...),
    cc_seq: int = Form(...),
    sc_seq: int = Form(...),
    gc_seq: int = Form(...),
    m_seq: int = Form(...),
    p_name: Optional[str] = Form(None),
    p_price: int = Form(0),
    p_stock: int = Form(0),
    p_image: Optional[str] = Form(None),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO product (kc_seq, cc_seq, sc_seq, gc_seq, m_seq, p_name, p_price, p_stock, p_image) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (kc_seq, cc_seq, sc_seq, gc_seq, m_seq, p_name, p_price, p_stock, p_image))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "p_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제품 수정
# ============================================
@app.post("/update_product")
async def update_product(
    p_seq: int = Form(...),
    kc_seq: int = Form(...),
    cc_seq: int = Form(...),
    sc_seq: int = Form(...),
    gc_seq: int = Form(...),
    m_seq: int = Form(...),
    p_name: Optional[str] = Form(None),
    p_price: int = Form(0),
    p_stock: int = Form(0),
    p_image: Optional[str] = Form(None),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE product 
            SET kc_seq=%s, cc_seq=%s, sc_seq=%s, gc_seq=%s, m_seq=%s, 
                p_name=%s, p_price=%s, p_stock=%s, p_image=%s 
            WHERE p_seq=%s
        """
        curs.execute(sql, (kc_seq, cc_seq, sc_seq, gc_seq, m_seq, p_name, p_price, p_stock, p_image, p_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제품 재고 수정
# ============================================
@app.post("/update_product_stock/{product_seq}")
async def update_product_stock(
    product_seq: int,
    p_stock: int = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE product SET p_stock=%s WHERE p_seq=%s"
        curs.execute(sql, (p_stock, product_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제품 삭제
# ============================================
@app.delete("/delete_product/{product_seq}")
async def delete_product(product_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM product WHERE p_seq=%s"
        curs.execute(sql, (product_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

