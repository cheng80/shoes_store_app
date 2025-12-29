"""
SizeCategory API - 사이즈 카테고리 CRUD
개별 실행: python size_category.py
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class SizeCategory(BaseModel):
    sc_seq: Optional[int] = None
    sc_name: str


# ============================================
# 전체 사이즈 카테고리 조회
# ============================================
@router.get("")
async def select_size_categories():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT sc_seq, sc_name 
        FROM size_category 
        ORDER BY sc_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'sc_seq': row[0],
        'sc_name': row[1]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 사이즈 카테고리 조회
# ============================================
@router.get("/{size_category_seq}")
async def select_size_category(size_category_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT sc_seq, sc_name 
        FROM size_category 
        WHERE sc_seq = %s
    """, (size_category_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "SizeCategory not found"}
    result = {
        'sc_seq': row[0],
        'sc_name': row[1]
    }
    return {"result": result}


# ============================================
# 사이즈 카테고리 추가
# ============================================
@router.post("")
async def insert_size_category(
    sc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO size_category (sc_name) VALUES (%s)"
        curs.execute(sql, (sc_name,))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "sc_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 사이즈 카테고리 수정
# ============================================
@router.post("/{id}")
async def update_size_category(
    sc_seq: int = Form(...),
    sc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE size_category SET sc_name=%s WHERE sc_seq=%s"
        curs.execute(sql, (sc_name, sc_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 사이즈 카테고리 삭제
# ============================================
@router.delete("/{size_category_seq}")
async def delete_size_category(size_category_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM size_category WHERE sc_seq=%s"
        curs.execute(sql, (size_category_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

