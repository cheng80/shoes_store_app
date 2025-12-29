"""
KindCategory API - 종류 카테고리 CRUD
개별 실행: python kind_category.py
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
class KindCategory(BaseModel):
    kc_seq: Optional[int] = None
    kc_name: str


# ============================================
# 전체 종류 카테고리 조회
# ============================================
@app.get("/select_kind_categories")
async def select_kind_categories():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT kc_seq, kc_name 
        FROM kind_category 
        ORDER BY kc_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'kc_seq': row[0],
        'kc_name': row[1]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 종류 카테고리 조회
# ============================================
@app.get("/select_kind_category/{kind_category_seq}")
async def select_kind_category(kind_category_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT kc_seq, kc_name 
        FROM kind_category 
        WHERE kc_seq = %s
    """, (kind_category_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "KindCategory not found"}
    result = {
        'kc_seq': row[0],
        'kc_name': row[1]
    }
    return {"result": result}


# ============================================
# 종류 카테고리 추가
# ============================================
@app.post("/insert_kind_category")
async def insert_kind_category(
    kc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO kind_category (kc_name) VALUES (%s)"
        curs.execute(sql, (kc_name,))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "kc_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 종류 카테고리 수정
# ============================================
@app.post("/update_kind_category")
async def update_kind_category(
    kc_seq: int = Form(...),
    kc_name: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE kind_category SET kc_name=%s WHERE kc_seq=%s"
        curs.execute(sql, (kc_name, kc_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 종류 카테고리 삭제
# ============================================
@app.delete("/delete_kind_category/{kind_category_seq}")
async def delete_kind_category(kind_category_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM kind_category WHERE kc_seq=%s"
        curs.execute(sql, (kind_category_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)

