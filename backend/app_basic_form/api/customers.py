"""
Customer API - 고객 CRUD (Form 방식)
RESTful 기본 CRUD + 프로필 이미지

Note: INSERT는 이미지 포함 필수, UPDATE는 이미지 제외/포함 두 가지 방식 제공
"""

from fastapi import APIRouter, Form, UploadFile, File, Response
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class Customer(BaseModel):
    id: Optional[int] = None
    cEmail: str
    cPhoneNumber: str
    cName: str
    cPassword: str


# ============================================
# 전체 고객 조회 (이미지 제외)
# ============================================
@router.get("")
async def select_customers():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cEmail, cPhoneNumber, cName, cPassword 
            FROM Customer 
            ORDER BY id
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'cEmail': row[1],
            'cPhoneNumber': row[2],
            'cName': row[3],
            'cPassword': row[4]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 고객 조회 (이미지 제외)
# ============================================
@router.get("/{customer_id}")
async def select_customer(customer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, cEmail, cPhoneNumber, cName, cPassword 
            FROM Customer 
            WHERE id = %s
        """, (customer_id,))
        row = curs.fetchone()
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
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 추가 (이미지 포함 필수 - Form + UploadFile)
# ============================================
@router.post("")
async def insert_customer(
    cEmail: str = Form(...),
    cPhoneNumber: str = Form(...),
    cName: str = Form(...),
    cPassword: str = Form(...),
    file: UploadFile = File(...)
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        # 파일 읽기
        image_data = await file.read()
        
        sql = """
            INSERT INTO Customer (cEmail, cPhoneNumber, cName, cPassword, cProfileImage) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (cEmail, cPhoneNumber, cName, cPassword, image_data))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 수정 (이미지 제외 - Form)
# ============================================
@router.post("/{customer_id}")
async def update_customer(
    customer_id: int,
    cEmail: str = Form(...),
    cPhoneNumber: str = Form(...),
    cName: str = Form(...),
    cPassword: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE Customer 
            SET cEmail=%s, cPhoneNumber=%s, cName=%s, cPassword=%s 
            WHERE id=%s
        """
        curs.execute(sql, (cEmail, cPhoneNumber, cName, cPassword, customer_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 수정 (이미지 포함 - Form + UploadFile)
# ============================================
@router.post("/{customer_id}/with_image")
async def update_customer_with_image(
    customer_id: int,
    cEmail: str = Form(...),
    cPhoneNumber: str = Form(...),
    cName: str = Form(...),
    cPassword: str = Form(...),
    file: UploadFile = File(...)
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        # 파일 읽기
        image_data = await file.read()
        
        sql = """
            UPDATE Customer 
            SET cEmail=%s, cPhoneNumber=%s, cName=%s, cPassword=%s, cProfileImage=%s 
            WHERE id=%s
        """
        curs.execute(sql, (cEmail, cPhoneNumber, cName, cPassword, image_data, customer_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 프로필 이미지 조회 (Response - 바이너리 직접 반환)
# ============================================
@router.get("/{customer_id}/profile_image")
async def view_customer_profile_image(customer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("SELECT cProfileImage FROM Customer WHERE id = %s", (customer_id,))
        row = curs.fetchone()
        
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
    finally:
        conn.close()


# ============================================
# 프로필 이미지 삭제
# ============================================
@router.delete("/{customer_id}/profile_image")
async def delete_customer_profile_image(customer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "UPDATE Customer SET cProfileImage=NULL WHERE id=%s"
        curs.execute(sql, (customer_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 고객 삭제
# ============================================
@router.delete("/{customer_id}")
async def delete_customer(customer_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM Customer WHERE id=%s"
        curs.execute(sql, (customer_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.customers (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Customer API Test")
    test_app.include_router(router, prefix="/api/customers")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

