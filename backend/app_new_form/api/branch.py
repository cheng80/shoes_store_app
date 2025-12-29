"""
Branch API - 지점 CRUD (Router 버전)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class Branch(BaseModel):
    br_seq: Optional[int] = None
    br_phone: Optional[str] = None
    br_address: Optional[str] = None
    br_name: str
    br_lat: Optional[float] = None
    br_lng: Optional[float] = None


# ============================================
# 전체 지점 조회
# ============================================
@router.get("")
async def select_branches():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT br_seq, br_phone, br_address, br_name, br_lat, br_lng 
            FROM branch 
            ORDER BY br_seq
        """)
        rows = curs.fetchall()
        result = [{
            'br_seq': row[0],
            'br_phone': row[1],
            'br_address': row[2],
            'br_name': row[3],
            'br_lat': float(row[4]) if row[4] else None,
            'br_lng': float(row[5]) if row[5] else None
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 지점 조회
# ============================================
@router.get("/{branch_seq}")
async def select_branch(branch_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT br_seq, br_phone, br_address, br_name, br_lat, br_lng 
            FROM branch 
            WHERE br_seq = %s
        """, (branch_seq,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "Branch not found"}
        result = {
            'br_seq': row[0],
            'br_phone': row[1],
            'br_address': row[2],
            'br_name': row[3],
            'br_lat': float(row[4]) if row[4] else None,
            'br_lng': float(row[5]) if row[5] else None
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 지점 추가
# ============================================
@router.post("")
async def insert_branch(
    br_name: str = Form(...),
    br_phone: Optional[str] = Form(None),
    br_address: Optional[str] = Form(None),
    br_lat: Optional[float] = Form(None),
    br_lng: Optional[float] = Form(None),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            INSERT INTO branch (br_name, br_phone, br_address, br_lat, br_lng) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (br_name, br_phone, br_address, br_lat, br_lng))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "br_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 지점 수정
# ============================================
@router.post("/{branch_seq}")
async def update_branch(
    branch_seq: int,
    br_name: str = Form(...),
    br_phone: Optional[str] = Form(None),
    br_address: Optional[str] = Form(None),
    br_lat: Optional[float] = Form(None),
    br_lng: Optional[float] = Form(None),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE branch 
            SET br_name=%s, br_phone=%s, br_address=%s, br_lat=%s, br_lng=%s 
            WHERE br_seq=%s
        """
        curs.execute(sql, (br_name, br_phone, br_address, br_lat, br_lng, branch_seq))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 지점 삭제
# ============================================
@router.delete("/{branch_seq}")
async def delete_branch(branch_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM branch WHERE br_seq=%s"
        curs.execute(sql, (branch_seq,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()

