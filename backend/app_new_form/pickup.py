"""
Pickup API - 오프라인 수령 CRUD
개별 실행: python pickup.py
"""

from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database.connection import connect_db

app = FastAPI()
ipAddress = "127.0.0.1"


# ============================================
# 모델 정의
# ============================================
class Pickup(BaseModel):
    pic_seq: Optional[int] = None
    b_seq: int
    pic_date: Optional[datetime] = None


# ============================================
# 전체 수령 내역 조회
# ============================================
@app.get("/select_pickups")
async def select_pickups():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT pic_seq, b_seq, pic_date 
        FROM pickup 
        ORDER BY pic_date DESC, pic_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'pic_seq': row[0],
        'b_seq': row[1],
        'pic_date': row[2].isoformat() if row[2] else None
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 수령 내역 조회
# ============================================
@app.get("/select_pickup/{pickup_seq}")
async def select_pickup(pickup_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT pic_seq, b_seq, pic_date 
        FROM pickup 
        WHERE pic_seq = %s
    """, (pickup_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Pickup not found"}
    result = {
        'pic_seq': row[0],
        'b_seq': row[1],
        'pic_date': row[2].isoformat() if row[2] else None
    }
    return {"result": result}


# ============================================
# 구매 ID로 수령 내역 조회
# ============================================
@app.get("/select_pickup_by_purchase/{purchase_seq}")
async def select_pickup_by_purchase(purchase_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT pic_seq, b_seq, pic_date 
        FROM pickup 
        WHERE b_seq = %s
    """, (purchase_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Pickup not found"}
    result = {
        'pic_seq': row[0],
        'b_seq': row[1],
        'pic_date': row[2].isoformat() if row[2] else None
    }
    return {"result": result}


# ============================================
# 수령 내역 추가
# ============================================
@app.post("/insert_pickup")
async def insert_pickup(
    b_seq: int = Form(...),
    pic_date: Optional[str] = Form(None),  # ISO format string
):
    try:
        pic_date_dt = None
        if pic_date:
            pic_date_dt = datetime.fromisoformat(pic_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO pickup (b_seq, pic_date) VALUES (%s, %s)"
        curs.execute(sql, (b_seq, pic_date_dt))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "pic_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 수령 내역 수정
# ============================================
@app.post("/update_pickup")
async def update_pickup(
    pic_seq: int = Form(...),
    b_seq: int = Form(...),
    pic_date: Optional[str] = Form(None),  # ISO format string
):
    try:
        pic_date_dt = None
        if pic_date:
            pic_date_dt = datetime.fromisoformat(pic_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE pickup SET b_seq=%s, pic_date=%s WHERE pic_seq=%s"
        curs.execute(sql, (b_seq, pic_date_dt, pic_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 수령 완료 처리 (날짜 업데이트)
# ============================================
@app.post("/complete_pickup/{pickup_seq}")
async def complete_pickup(pickup_seq: int):
    try:
        from datetime import datetime
        pic_date_dt = datetime.now()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE pickup SET pic_date=%s WHERE pic_seq=%s"
        curs.execute(sql, (pic_date_dt, pickup_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 수령 내역 삭제
# ============================================
@app.delete("/delete_pickup/{pickup_seq}")
async def delete_pickup(pickup_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM pickup WHERE pic_seq=%s"
        curs.execute(sql, (pickup_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

