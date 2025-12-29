"""
GenderCategory API - 성별 카테고리 CRUD
개별 실행: python gender_category.py
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class GenderCategory(BaseModel):
    gc_seq: Optional[int] = None
    gc_name: str


# ============================================
# 전체 성별 카테고리 조회
# ============================================
@router.get("")
async def select_gender_categories():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT gc_seq, gc_name 
        FROM gender_category 
        ORDER BY gc_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'gc_seq': row[0],
        'gc_name': row[1]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 성별 카테고리 조회
# ============================================
@router.get("/{gender_category_seq}")
async def select_gender_category(gender_category_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT gc_seq, gc_name 
        FROM gender_category 
        WHERE gc_seq = %s
    """, (gender_category_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "GenderCategory not found"}
    result = {
        'gc_seq': row[0],
        'gc_name': row[1]
    }
    return {"result": result}


# ============================================
# 성별 카테고리 추가
# ============================================
@router.post("")
async def insert_gender_category(
    gc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO gender_category (gc_name) VALUES (%s)"
        curs.execute(sql, (gc_name,))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "gc_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 성별 카테고리 수정
# ============================================
@router.post("/{id}")
async def update_gender_category(
    gc_seq: int = Form(...),
    gc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE gender_category SET gc_name=%s WHERE gc_seq=%s"
        curs.execute(sql, (gc_name, gc_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 성별 카테고리 삭제
# ============================================
@router.delete("/{gender_category_seq}")
async def delete_gender_category(gender_category_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM gender_category WHERE gc_seq=%s"
        curs.execute(sql, (gender_category_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

