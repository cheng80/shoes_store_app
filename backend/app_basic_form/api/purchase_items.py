"""
PurchaseItem API - 주문 항목 CRUD (Form 방식)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class PurchaseItem(BaseModel):
    id: Optional[int] = None
    pid: int
    pcid: int
    pcQuantity: int
    pcStatus: str


# ============================================
# 전체 주문 항목 조회
# ============================================
@router.get("")
async def select_purchase_items():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pid, pcid, pcQuantity, pcStatus 
            FROM PurchaseItem 
            ORDER BY id
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 ID로 항목 조회
# ============================================
@router.get("/by_pcid/{pcid}")
async def select_purchase_items_by_pcid(pcid: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pid, pcid, pcQuantity, pcStatus 
            FROM PurchaseItem 
            WHERE pcid = %s
            ORDER BY id
        """, (pcid,))
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 주문 항목 조회
# ============================================
@router.get("/{purchase_item_id}")
async def select_purchase_item(purchase_item_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pid, pcid, pcQuantity, pcStatus 
            FROM PurchaseItem 
            WHERE id = %s
        """, (purchase_item_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "PurchaseItem not found"}
        result = {
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4]
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 항목 추가
# ============================================
@router.post("")
async def insert_purchase_item(
    pid: int = Form(...),
    pcid: int = Form(...),
    pcQuantity: int = Form(...),
    pcStatus: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            INSERT INTO PurchaseItem (pid, pcid, pcQuantity, pcStatus) 
            VALUES (%s, %s, %s, %s)
        """
        curs.execute(sql, (pid, pcid, pcQuantity, pcStatus))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 항목 수정
# ============================================
@router.post("/{purchase_item_id}")
async def update_purchase_item(
    purchase_item_id: int,
    pid: int = Form(...),
    pcid: int = Form(...),
    pcQuantity: int = Form(...),
    pcStatus: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE PurchaseItem 
            SET pid=%s, pcid=%s, pcQuantity=%s, pcStatus=%s 
            WHERE id=%s
        """
        curs.execute(sql, (pid, pcid, pcQuantity, pcStatus, purchase_item_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 항목 상태만 수정
# ============================================
@router.post("/{purchase_item_id}/status")
async def update_purchase_item_status(
    purchase_item_id: int,
    pcStatus: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "UPDATE PurchaseItem SET pcStatus=%s WHERE id=%s"
        curs.execute(sql, (pcStatus, purchase_item_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 항목 삭제
# ============================================
@router.delete("/{purchase_item_id}")
async def delete_purchase_item(purchase_item_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM PurchaseItem WHERE id=%s"
        curs.execute(sql, (purchase_item_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.purchase_items (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="PurchaseItem API Test")
    test_app.include_router(router, prefix="/api/purchase_items")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

