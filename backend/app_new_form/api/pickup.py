"""
Pickup API - 오프라인 수령 CRUD
개별 실행: python pickup.py
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class Pickup(BaseModel):
    pic_seq: Optional[int] = None
    b_seq: int
    u_seq: int
    created_at: Optional[datetime] = None


# ============================================
# 전체 수령 내역 조회
# ============================================
@router.get("")
async def select_pickups():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT pic_seq, b_seq, u_seq, created_at 
        FROM pickup 
        ORDER BY created_at DESC, pic_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'pic_seq': row[0],
        'b_seq': row[1],
        'u_seq': row[2],
        'created_at': row[3].isoformat() if row[3] else None
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 수령 내역 조회
# ============================================
@router.get("/{pickup_seq}")
async def select_pickup(pickup_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT pic_seq, b_seq, u_seq, created_at 
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
        'u_seq': row[2],
        'created_at': row[3].isoformat() if row[3] else None
    }
    return {"result": result}


# ============================================
# 구매 ID로 수령 내역 조회
# ============================================
@router.get("/{purchase_seq}")
async def select_pickup_by_purchase(purchase_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT pic_seq, b_seq, u_seq, created_at 
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
        'u_seq': row[2],
        'created_at': row[3].isoformat() if row[3] else None
    }
    return {"result": result}


# ============================================
# 수령 내역 추가
# ============================================
@router.post("")
async def insert_pickup(
    b_seq: int = Form(...),
    u_seq: int = Form(...),
    created_at: Optional[str] = Form(None),  # ISO format string
):
    try:
        created_at_dt = None
        if created_at:
            created_at_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        if created_at_dt:
            sql = "INSERT INTO pickup (b_seq, u_seq, created_at) VALUES (%s, %s, %s)"
            curs.execute(sql, (b_seq, u_seq, created_at_dt))
        else:
            sql = "INSERT INTO pickup (b_seq, u_seq) VALUES (%s, %s)"
            curs.execute(sql, (b_seq, u_seq))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "pic_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 수령 내역 수정
# ============================================
@router.post("/{id}")
async def update_pickup(
    pic_seq: int = Form(...),
    b_seq: int = Form(...),
    u_seq: int = Form(...),
    created_at: Optional[str] = Form(None),  # ISO format string
):
    try:
        created_at_dt = None
        if created_at:
            created_at_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        if created_at_dt:
            sql = "UPDATE pickup SET b_seq=%s, u_seq=%s, created_at=%s WHERE pic_seq=%s"
            curs.execute(sql, (b_seq, u_seq, created_at_dt, pic_seq))
        else:
            sql = "UPDATE pickup SET b_seq=%s, u_seq=%s WHERE pic_seq=%s"
            curs.execute(sql, (b_seq, u_seq, pic_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 수령 완료 처리 (날짜 업데이트)
# ============================================
@router.post("/pickup_seq/complete")
async def complete_pickup(pickup_seq: int):
    try:
        from datetime import datetime
        created_at_dt = datetime.now()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE pickup SET created_at=%s WHERE pic_seq=%s"
        curs.execute(sql, (created_at_dt, pickup_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 수령 내역 삭제
# ============================================
@router.delete("/{pickup_seq}")
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

