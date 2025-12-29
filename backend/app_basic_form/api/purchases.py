"""
Purchase API - 주문 CRUD (Form 방식)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class Purchase(BaseModel):
    id: Optional[int] = None
    cid: Optional[int] = None
    pickupDate: str
    orderCode: str
    timeStamp: str


# ============================================
# 전체 주문 조회
# ============================================
@router.get("")
async def select_purchases():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cid, pickupDate, orderCode, timeStamp 
            FROM Purchase 
            ORDER BY timeStamp DESC
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'cid': row[1],
            'pickupDate': row[2],
            'orderCode': row[3],
            'timeStamp': row[4]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 ID로 주문 조회
# ============================================
@router.get("/by_cid/{cid}")
async def select_purchases_by_cid(cid: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cid, pickupDate, orderCode, timeStamp 
            FROM Purchase 
            WHERE cid = %s
            ORDER BY timeStamp DESC
        """, (cid,))
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'cid': row[1],
            'pickupDate': row[2],
            'orderCode': row[3],
            'timeStamp': row[4]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 주문 조회
# ============================================
@router.get("/{purchase_id}")
async def select_purchase(purchase_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cid, pickupDate, orderCode, timeStamp 
            FROM Purchase 
            WHERE id = %s
        """, (purchase_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "Purchase not found"}
        result = {
            'id': row[0],
            'cid': row[1],
            'pickupDate': row[2],
            'orderCode': row[3],
            'timeStamp': row[4]
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 추가
# ============================================
@router.post("")
async def insert_purchase(
    cid: int = Form(...),
    pickupDate: str = Form(...),
    orderCode: str = Form(...),
    timeStamp: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            INSERT INTO Purchase (cid, pickupDate, orderCode, timeStamp) 
            VALUES (%s, %s, %s, %s)
        """
        curs.execute(sql, (cid, pickupDate, orderCode, timeStamp))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 수정
# ============================================
@router.post("/{purchase_id}")
async def update_purchase(
    purchase_id: int,
    cid: int = Form(...),
    pickupDate: str = Form(...),
    orderCode: str = Form(...),
    timeStamp: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE Purchase 
            SET cid=%s, pickupDate=%s, orderCode=%s, timeStamp=%s 
            WHERE id=%s
        """
        curs.execute(sql, (cid, pickupDate, orderCode, timeStamp, purchase_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 삭제
# ============================================
@router.delete("/{purchase_id}")
async def delete_purchase(purchase_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM Purchase WHERE id=%s"
        curs.execute(sql, (purchase_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.purchases (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Purchase API Test")
    test_app.include_router(router, prefix="/api/purchases")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

