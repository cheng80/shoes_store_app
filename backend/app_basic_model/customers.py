"""
Customer API - 고객 CRUD (Model 방식)
개별 실행: python customers.py

Note: INSERT는 이미지 포함 필수, UPDATE는 이미지 제외/포함 두 가지 방식 제공
"""

from fastapi import FastAPI, UploadFile, File, Response, Form
from pydantic import BaseModel
from typing import Optional
from database.connection import connect_db

app = FastAPI()
ipAddress = "127.0.0.1"


# ============================================
# 모델 정의
# ============================================
class CustomerUpdate(BaseModel):
    id: int
    cEmail: str
    cPhoneNumber: str
    cName: str
    cPassword: str


# ============================================
# 전체 고객 조회 (이미지 제외)
# ============================================
@app.get("/select_customers")
async def select_customers():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cEmail, cPhoneNumber, cName, cPassword 
        FROM Customer 
        ORDER BY id
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'cEmail': row[1],
        'cPhoneNumber': row[2],
        'cName': row[3],
        'cPassword': row[4]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 고객 조회 (이미지 제외)
# ============================================
@app.get("/select_customer/{customer_id}")
async def select_customer(customer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, cEmail, cPhoneNumber, cName, cPassword 
        FROM Customer 
        WHERE id = %s
    """, (customer_id,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Customer not found"}
    
    result = {
        'id': row[0],
        'cEmail': row[1],
        'cPhoneNumber': row[2],
        'cName': row[3],
        'cPassword': row[4]
    }
    return {"result": result}


# ============================================
# 고객 추가 (이미지 포함 필수 - Form + UploadFile)
# ============================================
@app.post("/insert_customer")
async def insert_customer(
    cEmail: str = Form(...),
    cPhoneNumber: str = Form(...),
    cName: str = Form(...),
    cPassword: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO Customer (cEmail, cPhoneNumber, cName, cPassword, cProfileImage) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (cEmail, cPhoneNumber, cName, cPassword, image_data))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 수정 (이미지 제외 - JSON Body)
# ============================================
@app.post("/update_customer")
async def update_customer(customer: CustomerUpdate):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE Customer 
            SET cEmail=%s, cPhoneNumber=%s, cName=%s, cPassword=%s 
            WHERE id=%s
        """
        curs.execute(sql, (customer.cEmail, customer.cPhoneNumber, customer.cName, customer.cPassword, customer.id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 수정 (이미지 포함 - Form + UploadFile)
# ============================================
@app.post("/update_customer_with_image")
async def update_customer_with_image(
    customer_id: int = Form(...),
    cEmail: str = Form(...),
    cPhoneNumber: str = Form(...),
    cName: str = Form(...),
    cPassword: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE Customer 
            SET cEmail=%s, cPhoneNumber=%s, cName=%s, cPassword=%s, cProfileImage=%s 
            WHERE id=%s
        """
        curs.execute(sql, (cEmail, cPhoneNumber, cName, cPassword, image_data, customer_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 프로필 이미지 조회 (Response - 바이너리 직접 반환)
# ============================================
@app.get("/view_customer_profile_image/{customer_id}")
async def view_customer_profile_image(customer_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        curs.execute("SELECT cProfileImage FROM Customer WHERE id = %s", (customer_id,))
        row = curs.fetchone()
        conn.close()
        
        if row is None:
            return {"result": "Error", "message": "Customer not found"}
        
        if row[0] is None:
            return {"result": "Error", "message": "No profile image"}
        
        # Response 객체로 바이너리 직접 반환
        return Response(
            content=row[0],
            media_type="image/jpeg",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 프로필 이미지 삭제
# ============================================
@app.delete("/delete_customer_profile_image/{customer_id}")
async def delete_customer_profile_image(customer_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE Customer SET cProfileImage=NULL WHERE id=%s"
        curs.execute(sql, (customer_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 삭제
# ============================================
@app.delete("/delete_customer/{customer_id}")
async def delete_customer(customer_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM Customer WHERE id=%s"
        curs.execute(sql, (customer_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)
