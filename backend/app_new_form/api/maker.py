"""
Maker API - 제조사 CRUD
개별 실행: python maker.py
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class Maker(BaseModel):
    m_seq: Optional[int] = None
    m_name: str
    m_phone: Optional[str] = None
    m_address: Optional[str] = None


# ============================================
# 전체 제조사 조회
# ============================================
@router.get("")
async def select_makers():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT m_seq, m_name, m_phone, m_address 
        FROM maker 
        ORDER BY m_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'm_seq': row[0],
        'm_name': row[1],
        'm_phone': row[2],
        'm_address': row[3]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 제조사 조회
# ============================================
@router.get("/{maker_seq}")
async def select_maker(maker_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT m_seq, m_name, m_phone, m_address 
        FROM maker 
        WHERE m_seq = %s
    """, (maker_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Maker not found"}
    result = {
        'm_seq': row[0],
        'm_name': row[1],
        'm_phone': row[2],
        'm_address': row[3]
    }
    return {"result": result}


# ============================================
# 제조사 추가
# ============================================
@router.post("")
async def insert_maker(
    m_name: str = Form(...),
    m_phone: Optional[str] = Form(None),
    m_address: Optional[str] = Form(None),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO maker (m_name, m_phone, m_address) VALUES (%s, %s, %s)"
        curs.execute(sql, (m_name, m_phone, m_address))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "m_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제조사 수정
# ============================================
@router.post("/{id}")
async def update_maker(
    m_seq: int = Form(...),
    m_name: str = Form(...),
    m_phone: Optional[str] = Form(None),
    m_address: Optional[str] = Form(None),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE maker SET m_name=%s, m_phone=%s, m_address=%s WHERE m_seq=%s"
        curs.execute(sql, (m_name, m_phone, m_address, m_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제조사 삭제
# ============================================
@router.delete("/{maker_seq}")
async def delete_maker(maker_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM maker WHERE m_seq=%s"
        curs.execute(sql, (maker_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

