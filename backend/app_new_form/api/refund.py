"""
Refund API - 반품/환불 CRUD
개별 실행: python refund.py
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
class Refund(BaseModel):
    ref_seq: Optional[int] = None
    ref_date: Optional[datetime] = None
    ref_reason: Optional[str] = None
    ref_re_seq: Optional[int] = None
    ref_re_content: Optional[str] = None
    u_seq: int
    s_seq: int
    pic_seq: int


# ============================================
# 전체 반품 내역 조회
# ============================================
@router.get("")
async def select_refunds():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT ref_seq, ref_date, ref_reason, ref_re_seq, ref_re_content, u_seq, s_seq, pic_seq 
        FROM refund 
        ORDER BY ref_date DESC, ref_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'ref_seq': row[0],
        'ref_date': row[1].isoformat() if row[1] else None,
        'ref_reason': row[2],
        'ref_re_seq': row[3],
        'ref_re_content': row[4],
        'u_seq': row[5],
        's_seq': row[6],
        'pic_seq': row[7]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 반품 내역 조회
# ============================================
@router.get("/{refund_seq}")
async def select_refund(refund_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT ref_seq, ref_date, ref_reason, ref_re_seq, ref_re_content, u_seq, s_seq, pic_seq 
        FROM refund 
        WHERE ref_seq = %s
    """, (refund_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Refund not found"}
    result = {
        'ref_seq': row[0],
        'ref_date': row[1].isoformat() if row[1] else None,
        'ref_reason': row[2],
        'ref_re_seq': row[3],
        'ref_re_content': row[4],
        'u_seq': row[5],
        's_seq': row[6],
        'pic_seq': row[7]
    }
    return {"result": result}


# ============================================
# 고객별 반품 내역 조회
# ============================================
@router.get("/by_user/{user_seq}")
async def select_refunds_by_user(user_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT ref_seq, ref_date, ref_reason, ref_re_seq, ref_re_content, u_seq, s_seq, pic_seq 
        FROM refund 
        WHERE u_seq = %s
        ORDER BY ref_date DESC, ref_seq
    """, (user_seq,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'ref_seq': row[0],
        'ref_date': row[1].isoformat() if row[1] else None,
        'ref_reason': row[2],
        'ref_re_seq': row[3],
        'ref_re_content': row[4],
        'u_seq': row[5],
        's_seq': row[6],
        'pic_seq': row[7]
    } for row in rows]
    return {"results": result}


# ============================================
# 반품 내역 추가
# ============================================
@router.post("")
async def insert_refund(
    u_seq: int = Form(...),
    s_seq: int = Form(...),
    pic_seq: int = Form(...),
    ref_reason: Optional[str] = Form(None),
    ref_re_seq: Optional[int] = Form(None),
    ref_re_content: Optional[str] = Form(None),
    ref_date: Optional[str] = Form(None),  # ISO format string
):
    try:
        ref_date_dt = None
        if ref_date:
            ref_date_dt = datetime.fromisoformat(ref_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO refund (ref_date, ref_reason, ref_re_seq, ref_re_content, u_seq, s_seq, pic_seq) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (ref_date_dt, ref_reason, ref_re_seq, ref_re_content, u_seq, s_seq, pic_seq))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "ref_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 반품 내역 수정
# ============================================
@router.post("/{id}")
async def update_refund(
    ref_seq: int = Form(...),
    u_seq: int = Form(...),
    s_seq: int = Form(...),
    pic_seq: int = Form(...),
    ref_reason: Optional[str] = Form(None),
    ref_re_seq: Optional[int] = Form(None),
    ref_re_content: Optional[str] = Form(None),
    ref_date: Optional[str] = Form(None),  # ISO format string
):
    try:
        ref_date_dt = None
        if ref_date:
            ref_date_dt = datetime.fromisoformat(ref_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE refund 
            SET ref_date=%s, ref_reason=%s, ref_re_seq=%s, ref_re_content=%s, u_seq=%s, s_seq=%s, pic_seq=%s 
            WHERE ref_seq=%s
        """
        curs.execute(sql, (ref_date_dt, ref_reason, ref_re_seq, ref_re_content, u_seq, s_seq, pic_seq, ref_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 반품 처리 (날짜 업데이트)
# ============================================
@router.post("/{refund_seq}/process")
async def process_refund(refund_seq: int):
    try:
        ref_date_dt = datetime.now()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE refund SET ref_date=%s WHERE ref_seq=%s"
        curs.execute(sql, (ref_date_dt, refund_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 반품 내역 삭제
# ============================================
@router.delete("/{refund_seq}")
async def delete_refund(refund_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM refund WHERE ref_seq=%s"
        curs.execute(sql, (refund_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

