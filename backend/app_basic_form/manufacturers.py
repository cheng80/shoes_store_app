"""
Manufacturer API - 제조사 CRUD
개별 실행: python manufacturers.py
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
class Manufacturer(BaseModel):
    id: Optional[int] = None
    mName: str


# ============================================
# 전체 제조사 조회
# ============================================
@app.get("/select_manufacturers")
async def select_manufacturers():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, mName 
        FROM Manufacturer 
        ORDER BY id
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'mName': row[1]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 제조사 조회
# ============================================
@app.get("/select_manufacturer/{manufacturer_id}")
async def select_manufacturer(manufacturer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, mName 
        FROM Manufacturer 
        WHERE id = %s
    """, (manufacturer_id,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Manufacturer not found"}
    result = {
        'id': row[0],
        'mName': row[1]
    }
    return {"result": result}


# ============================================
# 제조사 추가
# ============================================
@app.post("/insert_manufacturer")
async def insert_manufacturer(
    mName: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO Manufacturer (mName) VALUES (%s)"
        curs.execute(sql, (mName,))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제조사 수정
# ============================================
@app.post("/update_manufacturer")
async def update_manufacturer(
    manufacturer_id: int = Form(...),
    mName: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE Manufacturer SET mName=%s WHERE id=%s"
        curs.execute(sql, (mName, manufacturer_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제조사 삭제
# ============================================
@app.delete("/delete_manufacturer/{manufacturer_id}")
async def delete_manufacturer(manufacturer_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM Manufacturer WHERE id=%s"
        curs.execute(sql, (manufacturer_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

