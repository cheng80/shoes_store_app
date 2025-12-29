"""
PurchaseItem API - 구매 내역 CRUD
개별 실행: python purchase_item.py

Note: b_tnum으로 여러 구매 항목을 하나의 주문으로 그룹화
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
class PurchaseItem(BaseModel):
    b_seq: Optional[int] = None
    br_seq: int
    u_seq: int
    p_seq: int
    b_price: int = 0
    b_quantity: int = 1
    b_date: datetime
    b_tnum: Optional[str] = None


# ============================================
# 전체 구매 내역 조회
# ============================================
@router.get("")
async def select_purchase_items():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT b_seq, br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum 
        FROM purchase_item 
        ORDER BY b_date DESC, b_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'b_seq': row[0],
        'br_seq': row[1],
        'u_seq': row[2],
        'p_seq': row[3],
        'b_price': row[4],
        'b_quantity': row[5],
        'b_date': row[6].isoformat() if row[6] else None,
        'b_tnum': row[7]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 구매 내역 조회
# ============================================
@router.get("/{purchase_item_seq}")
async def select_purchase_item(purchase_item_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT b_seq, br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum 
        FROM purchase_item 
        WHERE b_seq = %s
    """, (purchase_item_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "PurchaseItem not found"}
    result = {
        'b_seq': row[0],
        'br_seq': row[1],
        'u_seq': row[2],
        'p_seq': row[3],
        'b_price': row[4],
        'b_quantity': row[5],
        'b_date': row[6].isoformat() if row[6] else None,
        'b_tnum': row[7]
    }
    return {"result": result}


# ============================================
# 고객별 구매 내역 조회
# ============================================
@router.get("/{user_seq}")
async def select_purchase_items_by_user(user_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT b_seq, br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum 
        FROM purchase_item 
        WHERE u_seq = %s
        ORDER BY b_date DESC, b_seq
    """, (user_seq,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'b_seq': row[0],
        'br_seq': row[1],
        'u_seq': row[2],
        'p_seq': row[3],
        'b_price': row[4],
        'b_quantity': row[5],
        'b_date': row[6].isoformat() if row[6] else None,
        'b_tnum': row[7]
    } for row in rows]
    return {"results": result}


# ============================================
# 주문번호(b_tnum)로 구매 내역 조회 (주문 그룹화)
# ============================================
@router.get("")
async def select_purchase_items_by_tnum(b_tnum: str):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT b_seq, br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum 
        FROM purchase_item 
        WHERE b_tnum = %s
        ORDER BY b_seq
    """, (b_tnum,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'b_seq': row[0],
        'br_seq': row[1],
        'u_seq': row[2],
        'p_seq': row[3],
        'b_price': row[4],
        'b_quantity': row[5],
        'b_date': row[6].isoformat() if row[6] else None,
        'b_tnum': row[7]
    } for row in rows]
    return {"results": result}


# ============================================
# 구매 내역 추가
# ============================================
@router.post("")
async def insert_purchase_item(
    br_seq: int = Form(...),
    u_seq: int = Form(...),
    p_seq: int = Form(...),
    b_price: int = Form(0),
    b_quantity: int = Form(1),
    b_date: str = Form(...),  # ISO format string
    b_tnum: Optional[str] = Form(None),
):
    try:
        # 문자열을 datetime으로 변환
        b_date_dt = datetime.fromisoformat(b_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO purchase_item (br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (br_seq, u_seq, p_seq, b_price, b_quantity, b_date_dt, b_tnum))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "b_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 구매 내역 수정
# ============================================
@router.post("/{id}")
async def update_purchase_item(
    b_seq: int = Form(...),
    br_seq: int = Form(...),
    u_seq: int = Form(...),
    p_seq: int = Form(...),
    b_price: int = Form(0),
    b_quantity: int = Form(1),
    b_date: str = Form(...),  # ISO format string
    b_tnum: Optional[str] = Form(None),
):
    try:
        # 문자열을 datetime으로 변환
        b_date_dt = datetime.fromisoformat(b_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE purchase_item 
            SET br_seq=%s, u_seq=%s, p_seq=%s, b_price=%s, b_quantity=%s, b_date=%s, b_tnum=%s 
            WHERE b_seq=%s
        """
        curs.execute(sql, (br_seq, u_seq, p_seq, b_price, b_quantity, b_date_dt, b_tnum, b_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 구매 내역 삭제
# ============================================
@router.delete("/{purchase_item_seq}")
async def delete_purchase_item(purchase_item_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM purchase_item WHERE b_seq=%s"
        curs.execute(sql, (purchase_item_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

