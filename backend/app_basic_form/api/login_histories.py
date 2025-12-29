"""
LoginHistory API - 로그인 이력 CRUD (Form 방식)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class LoginHistory(BaseModel):
    id: Optional[int] = None
    cid: Optional[int] = None
    loginTime: str
    lStatus: str
    lVersion: float
    lAddress: str
    lPaymentMethod: str


# ============================================
# 전체 로그인 이력 조회
# ============================================
@router.get("")
async def select_login_histories():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
            FROM LoginHistory 
            ORDER BY id DESC
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'cid': row[1],
            'loginTime': row[2],
            'lStatus': row[3],
            'lVersion': row[4],
            'lAddress': row[5],
            'lPaymentMethod': row[6]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 ID로 로그인 이력 조회
# ============================================
@router.get("/by_cid/{cid}")
async def select_login_histories_by_cid(cid: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
            FROM LoginHistory 
            WHERE cid = %s
            ORDER BY id DESC
        """, (cid,))
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'cid': row[1],
            'loginTime': row[2],
            'lStatus': row[3],
            'lVersion': row[4],
            'lAddress': row[5],
            'lPaymentMethod': row[6]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 로그인 이력 조회
# ============================================
@router.get("/{login_history_id}")
async def select_login_history(login_history_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
            FROM LoginHistory 
            WHERE id = %s
        """, (login_history_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "LoginHistory not found"}
        result = {
            'id': row[0],
            'cid': row[1],
            'loginTime': row[2],
            'lStatus': row[3],
            'lVersion': row[4],
            'lAddress': row[5],
            'lPaymentMethod': row[6]
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 로그인 이력 추가
# ============================================
@router.post("")
async def insert_login_history(
    cid: int = Form(...),
    loginTime: str = Form(...),
    lStatus: str = Form(...),
    lVersion: float = Form(...),
    lAddress: str = Form(...),
    lPaymentMethod: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            INSERT INTO LoginHistory 
            (cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 로그인 이력 수정
# ============================================
@router.post("/{login_history_id}")
async def update_login_history(
    login_history_id: int,
    cid: int = Form(...),
    loginTime: str = Form(...),
    lStatus: str = Form(...),
    lVersion: float = Form(...),
    lAddress: str = Form(...),
    lPaymentMethod: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE LoginHistory 
            SET cid=%s, loginTime=%s, lStatus=%s, lVersion=%s, lAddress=%s, lPaymentMethod=%s 
            WHERE id=%s
        """
        curs.execute(sql, (cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod, login_history_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 ID로 상태만 수정
# ============================================
@router.post("/by_cid/{cid}/status")
async def update_status_by_cid(
    cid: int,
    lStatus: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "UPDATE LoginHistory SET lStatus=%s WHERE cid=%s"
        curs.execute(sql, (lStatus, cid))
        conn.commit()
        affected_rows = curs.rowcount
        return {"result": "OK", "affected_rows": affected_rows}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 ID로 로그인 시간만 수정
# ============================================
@router.post("/by_cid/{cid}/login_time")
async def update_login_time_by_cid(
    cid: int,
    loginTime: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "UPDATE LoginHistory SET loginTime=%s WHERE cid=%s"
        curs.execute(sql, (loginTime, cid))
        conn.commit()
        affected_rows = curs.rowcount
        return {"result": "OK", "affected_rows": affected_rows}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 로그인 이력 삭제
# ============================================
@router.delete("/{login_history_id}")
async def delete_login_history(login_history_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM LoginHistory WHERE id=%s"
        curs.execute(sql, (login_history_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.login_histories (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="LoginHistory API Test")
    test_app.include_router(router, prefix="/api/login_histories")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

