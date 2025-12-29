"""
Receive API - 입고(수주) CRUD
개별 실행: python receive.py
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
class Receive(BaseModel):
    rec_seq: Optional[int] = None
    rec_quantity: int = 0
    rec_date: Optional[datetime] = None
    s_seq: int
    p_seq: int
    m_seq: int


# ============================================
# 전체 입고 내역 조회
# ============================================
@router.get("")
async def select_receives():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT rec_seq, rec_quantity, rec_date, s_seq, p_seq, m_seq 
        FROM receive 
        ORDER BY rec_date DESC, rec_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'rec_seq': row[0],
        'rec_quantity': row[1],
        'rec_date': row[2].isoformat() if row[2] else None,
        's_seq': row[3],
        'p_seq': row[4],
        'm_seq': row[5]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 입고 내역 조회
# ============================================
@router.get("/{receive_seq}")
async def select_receive(receive_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT rec_seq, rec_quantity, rec_date, s_seq, p_seq, m_seq 
        FROM receive 
        WHERE rec_seq = %s
    """, (receive_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Receive not found"}
    result = {
        'rec_seq': row[0],
        'rec_quantity': row[1],
        'rec_date': row[2].isoformat() if row[2] else None,
        's_seq': row[3],
        'p_seq': row[4],
        'm_seq': row[5]
    }
    return {"result": result}


# ============================================
# 제품별 입고 내역 조회
# ============================================
@router.get("/{product_seq}")
async def select_receives_by_product(product_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT rec_seq, rec_quantity, rec_date, s_seq, p_seq, m_seq 
        FROM receive 
        WHERE p_seq = %s
        ORDER BY rec_date DESC, rec_seq
    """, (product_seq,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'rec_seq': row[0],
        'rec_quantity': row[1],
        'rec_date': row[2].isoformat() if row[2] else None,
        's_seq': row[3],
        'p_seq': row[4],
        'm_seq': row[5]
    } for row in rows]
    return {"results": result}


# ============================================
# 입고 내역 추가
# ============================================
@router.post("")
async def insert_receive(
    s_seq: int = Form(...),
    p_seq: int = Form(...),
    m_seq: int = Form(...),
    rec_quantity: int = Form(0),
    rec_date: Optional[str] = Form(None),  # ISO format string
):
    try:
        rec_date_dt = None
        if rec_date:
            rec_date_dt = datetime.fromisoformat(rec_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO receive (rec_quantity, rec_date, s_seq, p_seq, m_seq) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (rec_quantity, rec_date_dt, s_seq, p_seq, m_seq))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "rec_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 입고 내역 수정
# ============================================
@router.post("/{id}")
async def update_receive(
    rec_seq: int = Form(...),
    s_seq: int = Form(...),
    p_seq: int = Form(...),
    m_seq: int = Form(...),
    rec_quantity: int = Form(0),
    rec_date: Optional[str] = Form(None),  # ISO format string
):
    try:
        rec_date_dt = None
        if rec_date:
            rec_date_dt = datetime.fromisoformat(rec_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE receive 
            SET rec_quantity=%s, rec_date=%s, s_seq=%s, p_seq=%s, m_seq=%s 
            WHERE rec_seq=%s
        """
        curs.execute(sql, (rec_quantity, rec_date_dt, s_seq, p_seq, m_seq, rec_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 입고 처리 (날짜 업데이트)
# ============================================
@router.post("/receive_seq/process")
async def process_receive(receive_seq: int):
    try:
        rec_date_dt = datetime.now()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE receive SET rec_date=%s WHERE rec_seq=%s"
        curs.execute(sql, (rec_date_dt, receive_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 입고 내역 삭제
# ============================================
@router.delete("/{receive_seq}")
async def delete_receive(receive_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM receive WHERE rec_seq=%s"
        curs.execute(sql, (receive_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

