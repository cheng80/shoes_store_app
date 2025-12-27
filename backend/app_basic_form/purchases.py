"""
Purchase API - 주문 CRUD
개별 실행: python purchases.py
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
class Purchase(BaseModel):
    id: Optional[int] = None
    cid: Optional[int] = None
    pickupDate: str
    orderCode: str
    timeStamp: str


# ============================================
# 전체 주문 조회
# ============================================
@app.get("/select_purchases")
async def select_purchases():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cid, pickupDate, orderCode, timeStamp 
        FROM Purchase 
        ORDER BY timeStamp DESC
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'cid': row[1],
        'pickupDate': row[2],
        'orderCode': row[3],
        'timeStamp': row[4]
    } for row in rows]
    return {"results": result}


# ============================================
# 고객 ID로 주문 조회
# ============================================
@app.get("/select_purchases_by_cid/{cid}")
async def select_purchases_by_cid(cid: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cid, pickupDate, orderCode, timeStamp 
        FROM Purchase 
        WHERE cid = %s
        ORDER BY timeStamp DESC
    """, (cid,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'cid': row[1],
        'pickupDate': row[2],
        'orderCode': row[3],
        'timeStamp': row[4]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 주문 조회
# ============================================
@app.get("/select_purchase/{purchase_id}")
async def select_purchase(purchase_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cid, pickupDate, orderCode, timeStamp 
        FROM Purchase 
        WHERE id = %s
    """, (purchase_id,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Purchase not found"}
    result = {
        'id': row[0],
        'cid': row[1],
        'pickupDate': row[2],
        'orderCode': row[3],
        'timeStamp': row[4]
    }
    return {"result": result}


# ============================================
# 주문 추가
# ============================================
@app.post("/insert_purchase")
async def insert_purchase(
    cid: int = Form(...),
    pickupDate: str = Form(...),
    orderCode: str = Form(...),
    timeStamp: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO Purchase (cid, pickupDate, orderCode, timeStamp) 
            VALUES (%s, %s, %s, %s)
        """
        curs.execute(sql, (cid, pickupDate, orderCode, timeStamp))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 주문 수정
# ============================================
@app.post("/update_purchase")
async def update_purchase(
    purchase_id: int = Form(...),
    cid: int = Form(...),
    pickupDate: str = Form(...),
    orderCode: str = Form(...),
    timeStamp: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE Purchase 
            SET cid=%s, pickupDate=%s, orderCode=%s, timeStamp=%s 
            WHERE id=%s
        """
        curs.execute(sql, (cid, pickupDate, orderCode, timeStamp, purchase_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 주문 삭제
# ============================================
@app.delete("/delete_purchase/{purchase_id}")
async def delete_purchase(purchase_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM Purchase WHERE id=%s"
        curs.execute(sql, (purchase_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

