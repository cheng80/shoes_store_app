"""
ProductBase API - 제품 기본정보 CRUD
개별 실행: python product_bases.py
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
class ProductBase(BaseModel):
    id: Optional[int] = None
    pName: str
    pDescription: str
    pColor: str
    pGender: str
    pStatus: str
    pCategory: str
    pModelNumber: str


# ============================================
# 전체 ProductBase 조회
# ============================================
@app.get("/select_product_bases")
async def select_product_bases():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
        FROM ProductBase 
        ORDER BY id
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'pName': row[1],
        'pDescription': row[2],
        'pColor': row[3],
        'pGender': row[4],
        'pStatus': row[5],
        'pCategory': row[6],
        'pModelNumber': row[7]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 ProductBase 조회
# ============================================
@app.get("/select_product_base/{product_base_id}")
async def select_product_base(product_base_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
        FROM ProductBase 
        WHERE id = %s
    """, (product_base_id,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "ProductBase not found"}
    result = {
        'id': row[0],
        'pName': row[1],
        'pDescription': row[2],
        'pColor': row[3],
        'pGender': row[4],
        'pStatus': row[5],
        'pCategory': row[6],
        'pModelNumber': row[7]
    }
    return {"result": result}


# ============================================
# ProductBase 추가
# ============================================
@app.post("/insert_product_base")
async def insert_product_base(
    pName: str = Form(...),
    pDescription: str = Form(...),
    pColor: str = Form(...),
    pGender: str = Form(...),
    pStatus: str = Form(...),
    pCategory: str = Form(...),
    pModelNumber: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO ProductBase 
            (pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# ProductBase 수정
# ============================================
@app.post("/update_product_base")
async def update_product_base(
    product_base_id: int = Form(...),
    pName: str = Form(...),
    pDescription: str = Form(...),
    pColor: str = Form(...),
    pGender: str = Form(...),
    pStatus: str = Form(...),
    pCategory: str = Form(...),
    pModelNumber: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE ProductBase 
            SET pName=%s, pDescription=%s, pColor=%s, pGender=%s, pStatus=%s, pCategory=%s, pModelNumber=%s 
            WHERE id=%s
        """
        curs.execute(sql, (pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber, product_base_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# ProductBase 삭제
# ============================================
@app.delete("/delete_product_base/{product_base_id}")
async def delete_product_base(product_base_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM ProductBase WHERE id=%s"
        curs.execute(sql, (product_base_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

