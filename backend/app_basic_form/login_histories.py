"""
LoginHistory API - 로그인 이력 CRUD
개별 실행: python login_histories.py
"""

from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Optional
from database.connection import connect_db

app = FastAPI()
ipAddress = "127.0.0.1"


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
@app.get("/select_login_histories")
async def select_login_histories():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
        FROM LoginHistory 
        ORDER BY id DESC
    """)
    rows = curs.fetchall()
    conn.close()
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


# ============================================
# 고객 ID로 로그인 이력 조회
# ============================================
@app.get("/select_login_histories_by_cid/{cid}")
async def select_login_histories_by_cid(cid: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
        FROM LoginHistory 
        WHERE cid = %s
        ORDER BY id DESC
    """, (cid,))
    rows = curs.fetchall()
    conn.close()
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


# ============================================
# ID로 로그인 이력 조회
# ============================================
@app.get("/select_login_history/{login_history_id}")
async def select_login_history(login_history_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
        FROM LoginHistory 
        WHERE id = %s
    """, (login_history_id,))
    row = curs.fetchone()
    conn.close()
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


# ============================================
# 로그인 이력 추가
# ============================================
@app.post("/insert_login_history")
async def insert_login_history(
    cid: int = Form(...),
    loginTime: str = Form(...),
    lStatus: str = Form(...),
    lVersion: float = Form(...),
    lAddress: str = Form(...),
    lPaymentMethod: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO LoginHistory 
            (cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 로그인 이력 수정
# ============================================
@app.post("/update_login_history")
async def update_login_history(
    login_history_id: int = Form(...),
    cid: int = Form(...),
    loginTime: str = Form(...),
    lStatus: str = Form(...),
    lVersion: float = Form(...),
    lAddress: str = Form(...),
    lPaymentMethod: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE LoginHistory 
            SET cid=%s, loginTime=%s, lStatus=%s, lVersion=%s, lAddress=%s, lPaymentMethod=%s 
            WHERE id=%s
        """
        curs.execute(sql, (cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod, login_history_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 ID로 상태만 수정
# ============================================
@app.post("/update_status_by_cid/{cid}")
async def update_status_by_cid(
    cid: int,
    lStatus: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE LoginHistory SET lStatus=%s WHERE cid=%s"
        curs.execute(sql, (lStatus, cid))
        conn.commit()
        affected_rows = curs.rowcount
        conn.close()
        return {"result": "OK", "affected_rows": affected_rows}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 ID로 로그인 시간만 수정
# ============================================
@app.post("/update_login_time_by_cid/{cid}")
async def update_login_time_by_cid(
    cid: int,
    loginTime: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE LoginHistory SET loginTime=%s WHERE cid=%s"
        curs.execute(sql, (loginTime, cid))
        conn.commit()
        affected_rows = curs.rowcount
        conn.close()
        return {"result": "OK", "affected_rows": affected_rows}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 로그인 이력 삭제
# ============================================
@app.delete("/delete_login_history/{login_history_id}")
async def delete_login_history(login_history_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM LoginHistory WHERE id=%s"
        curs.execute(sql, (login_history_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

