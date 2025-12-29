"""
Branch API - 지점 CRUD
개별 실행: python branch.py
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
@app.get("/select_branches")
async def select_branches():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT br_seq, br_phone, br_address, br_name, br_lat, br_lng 
        FROM branch 
        ORDER BY br_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'br_seq': row[0],
        'br_phone': row[1],
        'br_address': row[2],
        'br_name': row[3],
        'br_lat': float(row[4]) if row[4] else None,
        'br_lng': float(row[5]) if row[5] else None
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 지점 조회
# ============================================
@app.get("/select_branch/{branch_seq}")
async def select_branch(branch_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT br_seq, br_phone, br_address, br_name, br_lat, br_lng 
        FROM branch 
        WHERE br_seq = %s
    """, (branch_seq,))
    row = curs.fetchone()
    conn.close()
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


# ============================================
# 지점 추가
# ============================================
@app.post("/insert_branch")
async def insert_branch(
    br_name: str = Form(...),
    br_phone: Optional[str] = Form(None),
    br_address: Optional[str] = Form(None),
    br_lat: Optional[float] = Form(None),
    br_lng: Optional[float] = Form(None),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO branch (br_name, br_phone, br_address, br_lat, br_lng) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (br_name, br_phone, br_address, br_lat, br_lng))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "br_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 지점 수정
# ============================================
@app.post("/update_branch")
async def update_branch(
    br_seq: int = Form(...),
    br_name: str = Form(...),
    br_phone: Optional[str] = Form(None),
    br_address: Optional[str] = Form(None),
    br_lat: Optional[float] = Form(None),
    br_lng: Optional[float] = Form(None),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE branch 
            SET br_name=%s, br_phone=%s, br_address=%s, br_lat=%s, br_lng=%s 
            WHERE br_seq=%s
        """
        curs.execute(sql, (br_name, br_phone, br_address, br_lat, br_lng, br_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 지점 삭제
# ============================================
@app.delete("/delete_branch/{branch_seq}")
async def delete_branch(branch_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM branch WHERE br_seq=%s"
        curs.execute(sql, (branch_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

