"""
Manufacturer API - 제조사 CRUD (Form 방식)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class Manufacturer(BaseModel):
    id: Optional[int] = None
    mName: str


# ============================================
# 전체 제조사 조회
# ============================================
@router.get("")
async def select_manufacturers():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, mName 
            FROM Manufacturer 
            ORDER BY id
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'mName': row[1]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 제조사 조회
# ============================================
@router.get("/{manufacturer_id}")
async def select_manufacturer(manufacturer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, mName 
            FROM Manufacturer 
            WHERE id = %s
        """, (manufacturer_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "Manufacturer not found"}
        result = {
            'id': row[0],
            'mName': row[1]
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제조사 추가
# ============================================
@router.post("")
async def insert_manufacturer(
    mName: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "INSERT INTO Manufacturer (mName) VALUES (%s)"
        curs.execute(sql, (mName,))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제조사 수정
# ============================================
@router.post("/{manufacturer_id}")
async def update_manufacturer(
    manufacturer_id: int,
    mName: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "UPDATE Manufacturer SET mName=%s WHERE id=%s"
        curs.execute(sql, (mName, manufacturer_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 제조사 삭제
# ============================================
@router.delete("/{manufacturer_id}")
async def delete_manufacturer(manufacturer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM Manufacturer WHERE id=%s"
        curs.execute(sql, (manufacturer_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.manufacturers (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Manufacturer API Test")
    test_app.include_router(router, prefix="/api/manufacturers")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

