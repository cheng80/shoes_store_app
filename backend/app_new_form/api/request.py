"""
Request API - 발주/품의 CRUD
개별 실행: python request.py
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
class Request(BaseModel):
    req_seq: Optional[int] = None
    req_date: Optional[datetime] = None
    req_content: Optional[str] = None
    req_quantity: int = 0
    req_manappdate: Optional[datetime] = None
    req_dirappdate: Optional[datetime] = None
    s_seq: int
    p_seq: int
    m_seq: int
    s_superseq: Optional[int] = None


# ============================================
# 전체 발주 내역 조회
# ============================================
@router.get("")
async def select_requests():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT req_seq, req_date, req_content, req_quantity, req_manappdate, req_dirappdate, 
               s_seq, p_seq, m_seq, s_superseq 
        FROM request 
        ORDER BY req_date DESC, req_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'req_seq': row[0],
        'req_date': row[1].isoformat() if row[1] else None,
        'req_content': row[2],
        'req_quantity': row[3],
        'req_manappdate': row[4].isoformat() if row[4] else None,
        'req_dirappdate': row[5].isoformat() if row[5] else None,
        's_seq': row[6],
        'p_seq': row[7],
        'm_seq': row[8],
        's_superseq': row[9]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 발주 내역 조회
# ============================================
@router.get("/{request_seq}")
async def select_request(request_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT req_seq, req_date, req_content, req_quantity, req_manappdate, req_dirappdate, 
               s_seq, p_seq, m_seq, s_superseq 
        FROM request 
        WHERE req_seq = %s
    """, (request_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Request not found"}
    result = {
        'req_seq': row[0],
        'req_date': row[1].isoformat() if row[1] else None,
        'req_content': row[2],
        'req_quantity': row[3],
        'req_manappdate': row[4].isoformat() if row[4] else None,
        'req_dirappdate': row[5].isoformat() if row[5] else None,
        's_seq': row[6],
        'p_seq': row[7],
        'm_seq': row[8],
        's_superseq': row[9]
    }
    return {"result": result}


# ============================================
# 발주 내역 추가
# ============================================
@router.post("")
async def insert_request(
    s_seq: int = Form(...),
    p_seq: int = Form(...),
    m_seq: int = Form(...),
    req_content: Optional[str] = Form(None),
    req_quantity: int = Form(0),
    req_date: Optional[str] = Form(None),  # ISO format string
    req_manappdate: Optional[str] = Form(None),  # ISO format string
    req_dirappdate: Optional[str] = Form(None),  # ISO format string
    s_superseq: Optional[int] = Form(None),
):
    try:
        req_date_dt = None
        if req_date:
            req_date_dt = datetime.fromisoformat(req_date.replace('Z', '+00:00'))
        
        req_manappdate_dt = None
        if req_manappdate:
            req_manappdate_dt = datetime.fromisoformat(req_manappdate.replace('Z', '+00:00'))
        
        req_dirappdate_dt = None
        if req_dirappdate:
            req_dirappdate_dt = datetime.fromisoformat(req_dirappdate.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO request (req_date, req_content, req_quantity, req_manappdate, req_dirappdate, 
                               s_seq, p_seq, m_seq, s_superseq) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (req_date_dt, req_content, req_quantity, req_manappdate_dt, req_dirappdate_dt, 
                          s_seq, p_seq, m_seq, s_superseq))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "req_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 발주 내역 수정
# ============================================
@router.post("/{id}")
async def update_request(
    req_seq: int = Form(...),
    s_seq: int = Form(...),
    p_seq: int = Form(...),
    m_seq: int = Form(...),
    req_content: Optional[str] = Form(None),
    req_quantity: int = Form(0),
    req_date: Optional[str] = Form(None),  # ISO format string
    req_manappdate: Optional[str] = Form(None),  # ISO format string
    req_dirappdate: Optional[str] = Form(None),  # ISO format string
    s_superseq: Optional[int] = Form(None),
):
    try:
        req_date_dt = None
        if req_date:
            req_date_dt = datetime.fromisoformat(req_date.replace('Z', '+00:00'))
        
        req_manappdate_dt = None
        if req_manappdate:
            req_manappdate_dt = datetime.fromisoformat(req_manappdate.replace('Z', '+00:00'))
        
        req_dirappdate_dt = None
        if req_dirappdate:
            req_dirappdate_dt = datetime.fromisoformat(req_dirappdate.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE request 
            SET req_date=%s, req_content=%s, req_quantity=%s, req_manappdate=%s, req_dirappdate=%s, 
                s_seq=%s, p_seq=%s, m_seq=%s, s_superseq=%s 
            WHERE req_seq=%s
        """
        curs.execute(sql, (req_date_dt, req_content, req_quantity, req_manappdate_dt, req_dirappdate_dt, 
                          s_seq, p_seq, m_seq, s_superseq, req_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 팀장 결재 처리
# ============================================
@router.post("/request_seq/approve_manager")
async def approve_request_manager(request_seq: int):
    try:
        req_manappdate_dt = datetime.now()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE request SET req_manappdate=%s WHERE req_seq=%s"
        curs.execute(sql, (req_manappdate_dt, request_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 이사 결재 처리
# ============================================
@router.post("/request_seq/approve_director")
async def approve_request_director(request_seq: int):
    try:
        req_dirappdate_dt = datetime.now()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE request SET req_dirappdate=%s WHERE req_seq=%s"
        curs.execute(sql, (req_dirappdate_dt, request_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 발주 내역 삭제
# ============================================
@router.delete("/{request_seq}")
async def delete_request(request_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM request WHERE req_seq=%s"
        curs.execute(sql, (request_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

