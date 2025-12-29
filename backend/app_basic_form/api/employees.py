"""
Employee API - 직원 CRUD (Form 방식)
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
class Employee(BaseModel):
    id: Optional[int] = None
    eEmail: str
    ePhoneNumber: str
    eName: str
    ePassword: str
    eRole: str


# ============================================
# 전체 직원 조회 (이미지 제외)
# ============================================
@router.get("")
async def select_employees():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, eEmail, ePhoneNumber, eName, ePassword, eRole 
            FROM Employee 
            ORDER BY id
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'eEmail': row[1],
            'ePhoneNumber': row[2],
            'eName': row[3],
            'ePassword': row[4],
            'eRole': row[5]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 직원 조회 (이미지 제외)
# ============================================
@router.get("/{employee_id}")
async def select_employee(employee_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, eEmail, ePhoneNumber, eName, ePassword, eRole 
            FROM Employee 
            WHERE id = %s
        """, (employee_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "Employee not found"}
        
        result = {
            'id': row[0],
            'eEmail': row[1],
            'ePhoneNumber': row[2],
            'eName': row[3],
            'ePassword': row[4],
            'eRole': row[5]
        }
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 직원 추가 (이미지 포함 필수 - Form + UploadFile)
# ============================================
@router.post("")
async def insert_employee(
    eEmail: str = Form(...),
    ePhoneNumber: str = Form(...),
    eName: str = Form(...),
    ePassword: str = Form(...),
    eRole: str = Form(...),
    file: UploadFile = File(...)
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        # 파일 읽기
        image_data = await file.read()
        
        sql = """
            INSERT INTO Employee (eEmail, ePhoneNumber, eName, ePassword, eRole, eProfileImage) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (eEmail, ePhoneNumber, eName, ePassword, eRole, image_data))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 직원 수정 (이미지 제외 - Form)
# ============================================
@router.post("/{employee_id}")
async def update_employee(
    employee_id: int,
    eEmail: str = Form(...),
    ePhoneNumber: str = Form(...),
    eName: str = Form(...),
    ePassword: str = Form(...),
    eRole: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE Employee 
            SET eEmail=%s, ePhoneNumber=%s, eName=%s, ePassword=%s, eRole=%s 
            WHERE id=%s
        """
        curs.execute(sql, (eEmail, ePhoneNumber, eName, ePassword, eRole, employee_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 직원 수정 (이미지 포함 - Form + UploadFile)
# ============================================
@router.post("/{employee_id}/with_image")
async def update_employee_with_image(
    employee_id: int,
    eEmail: str = Form(...),
    ePhoneNumber: str = Form(...),
    eName: str = Form(...),
    ePassword: str = Form(...),
    eRole: str = Form(...),
    file: UploadFile = File(...)
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        # 파일 읽기
        image_data = await file.read()
        
        sql = """
            UPDATE Employee 
            SET eEmail=%s, ePhoneNumber=%s, eName=%s, ePassword=%s, eRole=%s, eProfileImage=%s 
            WHERE id=%s
        """
        curs.execute(sql, (eEmail, ePhoneNumber, eName, ePassword, eRole, image_data, employee_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 프로필 이미지 조회 (Response - 바이너리 직접 반환)
# ============================================
@router.get("/{employee_id}/profile_image")
async def view_employee_profile_image(employee_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("SELECT eProfileImage FROM Employee WHERE id = %s", (employee_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Employee not found"}
        
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
@router.delete("/{employee_id}/profile_image")
async def delete_employee_profile_image(employee_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "UPDATE Employee SET eProfileImage=NULL WHERE id=%s"
        curs.execute(sql, (employee_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 직원 삭제
# ============================================
@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM Employee WHERE id=%s"
        curs.execute(sql, (employee_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.employees (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Employee API Test")
    test_app.include_router(router, prefix="/api/employees")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

