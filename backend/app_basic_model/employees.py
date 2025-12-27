"""
Employee API - 직원 CRUD (Model 방식)
개별 실행: python employees.py

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
class EmployeeUpdate(BaseModel):
    id: int
    eEmail: str
    ePhoneNumber: str
    eName: str
    ePassword: str
    eRole: str


# ============================================
# 전체 직원 조회 (이미지 제외)
# ============================================
@app.get("/select_employees")
async def select_employees():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, eEmail, ePhoneNumber, eName, ePassword, eRole 
        FROM Employee 
        ORDER BY id
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'eEmail': row[1],
        'ePhoneNumber': row[2],
        'eName': row[3],
        'ePassword': row[4],
        'eRole': row[5]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 직원 조회 (이미지 제외)
# ============================================
@app.get("/select_employee/{employee_id}")
async def select_employee(employee_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, eEmail, ePhoneNumber, eName, ePassword, eRole 
        FROM Employee 
        WHERE id = %s
    """, (employee_id,))
    row = curs.fetchone()
    conn.close()
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


# ============================================
# 직원 추가 (이미지 포함 필수 - Form + UploadFile)
# ============================================
@app.post("/insert_employee")
async def insert_employee(
    eEmail: str = Form(...),
    ePhoneNumber: str = Form(...),
    eName: str = Form(...),
    ePassword: str = Form(...),
    eRole: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO Employee (eEmail, ePhoneNumber, eName, ePassword, eRole, eProfileImage) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (eEmail, ePhoneNumber, eName, ePassword, eRole, image_data))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 직원 수정 (이미지 제외 - JSON Body)
# ============================================
@app.post("/update_employee")
async def update_employee(employee: EmployeeUpdate):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE Employee 
            SET eEmail=%s, ePhoneNumber=%s, eName=%s, ePassword=%s, eRole=%s 
            WHERE id=%s
        """
        curs.execute(sql, (employee.eEmail, employee.ePhoneNumber, employee.eName, employee.ePassword, employee.eRole, employee.id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 직원 수정 (이미지 포함 - Form + UploadFile)
# ============================================
@app.post("/update_employee_with_image")
async def update_employee_with_image(
    employee_id: int = Form(...),
    eEmail: str = Form(...),
    ePhoneNumber: str = Form(...),
    eName: str = Form(...),
    ePassword: str = Form(...),
    eRole: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE Employee 
            SET eEmail=%s, ePhoneNumber=%s, eName=%s, ePassword=%s, eRole=%s, eProfileImage=%s 
            WHERE id=%s
        """
        curs.execute(sql, (eEmail, ePhoneNumber, eName, ePassword, eRole, image_data, employee_id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 프로필 이미지 조회 (Response - 바이너리 직접 반환)
# ============================================
@app.get("/view_employee_profile_image/{employee_id}")
async def view_employee_profile_image(employee_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        curs.execute("SELECT eProfileImage FROM Employee WHERE id = %s", (employee_id,))
        row = curs.fetchone()
        conn.close()
        
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


# ============================================
# 프로필 이미지 삭제
# ============================================
@app.delete("/delete_employee_profile_image/{employee_id}")
async def delete_employee_profile_image(employee_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE Employee SET eProfileImage=NULL WHERE id=%s"
        curs.execute(sql, (employee_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 직원 삭제
# ============================================
@app.delete("/delete_employee/{employee_id}")
async def delete_employee(employee_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM Employee WHERE id=%s"
        curs.execute(sql, (employee_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)
