"""
PurchaseItem API - 주문 항목 CRUD (Model 방식)
개별 실행: python purchase_items.py
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from database.connection import connect_db

app = FastAPI()
ipAddress = "127.0.0.1"


# ============================================
# 모델 정의
# ============================================
class PurchaseItemCreate(BaseModel):
    pid: int
    pcid: int
    pcQuantity: int
    pcStatus: str


class PurchaseItemUpdate(BaseModel):
    id: int
    pid: int
    pcid: int
    pcQuantity: int
    pcStatus: str


class PurchaseItemStatusUpdate(BaseModel):
    pcStatus: str


# ============================================
# 전체 주문 항목 조회
# ============================================
@app.get("/select_purchase_items")
async def select_purchase_items():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pid, pcid, pcQuantity, pcStatus 
        FROM PurchaseItem 
        ORDER BY id
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'pid': row[1],
        'pcid': row[2],
        'pcQuantity': row[3],
        'pcStatus': row[4]
    } for row in rows]
    return {"results": result}


# ============================================
# 주문 ID로 항목 조회
# ============================================
@app.get("/select_purchase_items_by_pcid/{pcid}")
async def select_purchase_items_by_pcid(pcid: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pid, pcid, pcQuantity, pcStatus 
        FROM PurchaseItem 
        WHERE pcid = %s
        ORDER BY id
    """, (pcid,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'pid': row[1],
        'pcid': row[2],
        'pcQuantity': row[3],
        'pcStatus': row[4]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 주문 항목 조회
# ============================================
@app.get("/select_purchase_item/{purchase_item_id}")
async def select_purchase_item(purchase_item_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pid, pcid, pcQuantity, pcStatus 
        FROM PurchaseItem 
        WHERE id = %s
    """, (purchase_item_id,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "PurchaseItem not found"}
    result = {
        'id': row[0],
        'pid': row[1],
        'pcid': row[2],
        'pcQuantity': row[3],
        'pcStatus': row[4]
    }
    return {"result": result}


# ============================================
# 주문 항목 추가 (JSON Body)
# ============================================
@app.post("/insert_purchase_item")
async def insert_purchase_item(item: PurchaseItemCreate):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO PurchaseItem (pid, pcid, pcQuantity, pcStatus) 
            VALUES (%s, %s, %s, %s)
        """
        curs.execute(sql, (item.pid, item.pcid, item.pcQuantity, item.pcStatus))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 주문 항목 수정 (JSON Body)
# ============================================
@app.post("/update_purchase_item")
async def update_purchase_item(item: PurchaseItemUpdate):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE PurchaseItem 
            SET pid=%s, pcid=%s, pcQuantity=%s, pcStatus=%s 
            WHERE id=%s
        """
        curs.execute(sql, (item.pid, item.pcid, item.pcQuantity, item.pcStatus, item.id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 주문 항목 상태만 수정 (JSON Body)
# ============================================
@app.post("/update_purchase_item_status/{purchase_item_id}")
async def update_purchase_item_status(purchase_item_id: int, status: PurchaseItemStatusUpdate):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE PurchaseItem SET pcStatus=%s WHERE id=%s"
        curs.execute(sql, (status.pcStatus, purchase_item_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 주문 항목 삭제
# ============================================
@app.delete("/delete_purchase_item/{purchase_item_id}")
async def delete_purchase_item(purchase_item_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM PurchaseItem WHERE id=%s"
        curs.execute(sql, (purchase_item_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)
