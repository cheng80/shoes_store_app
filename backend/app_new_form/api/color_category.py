"""
ColorCategory API - 색상 카테고리 CRUD
개별 실행: python color_category.py
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class ColorCategory(BaseModel):
    cc_seq: Optional[int] = None
    cc_name: str


# ============================================
# 전체 색상 카테고리 조회
# ============================================
@router.get("")
async def select_color_categories():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT cc_seq, cc_name 
        FROM color_category 
        ORDER BY cc_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'cc_seq': row[0],
        'cc_name': row[1]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 색상 카테고리 조회
# ============================================
@router.get("/{color_category_seq}")
async def select_color_category(color_category_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT cc_seq, cc_name 
        FROM color_category 
        WHERE cc_seq = %s
    """, (color_category_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "ColorCategory not found"}
    result = {
        'cc_seq': row[0],
        'cc_name': row[1]
    }
    return {"result": result}


# ============================================
# 색상 카테고리 추가
# ============================================
@router.post("")
async def insert_color_category(
    cc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO color_category (cc_name) VALUES (%s)"
        curs.execute(sql, (cc_name,))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "cc_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 색상 카테고리 수정
# ============================================
@router.post("/{id}")
async def update_color_category(
    cc_seq: int = Form(...),
    cc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE color_category SET cc_name=%s WHERE cc_seq=%s"
        curs.execute(sql, (cc_name, cc_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 색상 카테고리 삭제
# ============================================
@router.delete("/{color_category_seq}")
async def delete_color_category(color_category_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM color_category WHERE cc_seq=%s"
        curs.execute(sql, (color_category_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

