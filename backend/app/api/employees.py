"""
Employee API
RESTful 기본 CRUD + 필터링 + 프로필 이미지

Note: INSERT는 이미지 포함 필수, UPDATE는 이미지 제외/포함 두 가지 방식 제공
"""

from fastapi import APIRouter, Query, UploadFile, File, Response, Form
from typing import Optional
from app.models.all_models import Employee
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_employees(
    email: Optional[str] = Query(None, description="이메일로 필터"),
    phone: Optional[str] = Query(None, description="전화번호로 필터"),
    identifier: Optional[str] = Query(None, description="이메일 또는 전화번호로 필터 (OR 조건)"),
    role: Optional[str] = Query(None, description="역할로 필터"),
    order_by: str = Query("id", description="정렬 기준"),
    order: str = Query("asc", description="정렬 방향 (asc, desc)")
):
    """직원 조회 (필터링 및 정렬 가능, 이미지 제외)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        conditions = []
        params = []
        
        if identifier:
            # 이메일 또는 전화번호로 검색 (OR 조건)
            conditions.append("(eEmail = %s OR ePhoneNumber = %s)")
            params.extend([identifier, identifier])
        else:
            if email:
                conditions.append("eEmail = %s")
                params.append(email)
            if phone:
                conditions.append("ePhoneNumber = %s")
                params.append(phone)
        
        if role:
            conditions.append("eRole = %s")
            params.append(role)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        
        sql = f"""
        SELECT id, eEmail, ePhoneNumber, eName, ePassword, eRole 
        FROM Employee 
        WHERE {where_clause}
        ORDER BY {order_by} {order_direction}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'eEmail': row[1],
                'ePhoneNumber': row[2],
                'eName': row[3],
                'ePassword': row[4],
                'eRole': row[5]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{employee_id}")
async def get_employee(employee_id: int):
    """ID로 직원 조회 (이미지 제외)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, eEmail, ePhoneNumber, eName, ePassword, eRole FROM Employee WHERE id = %s"
        curs.execute(sql, (employee_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Employee not found'}
        
        result = {
            'id': row[0],
            'eEmail': row[1],
            'ePhoneNumber': row[2],
            'eName': row[3],
            'ePassword': row[4],
            'eRole': row[5]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_employee(
    eEmail: str = Form(...),
    ePhoneNumber: str = Form(...),
    eName: str = Form(...),
    ePassword: str = Form(...),
    eRole: str = Form(...),
    file: UploadFile = File(...)
):
    """직원 생성 (이미지 포함 필수)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 파일 읽기
        image_data = await file.read()
        
        sql = """
        INSERT INTO Employee 
        (eEmail, ePhoneNumber, eName, ePassword, eRole, eProfileImage)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (
            eEmail,
            ePhoneNumber,
            eName,
            ePassword,
            eRole,
            image_data
        ))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{employee_id}")
async def update_employee(employee_id: int, employee: Employee):
    """직원 수정 (이미지 제외)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        UPDATE Employee
        SET eEmail=%s, ePhoneNumber=%s, eName=%s, ePassword=%s, eRole=%s
        WHERE id=%s
        """
        curs.execute(sql, (
            employee.eEmail,
            employee.ePhoneNumber,
            employee.eName,
            employee.ePassword,
            employee.eRole,
            employee_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


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
    """직원 수정 (이미지 포함)"""
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
        curs.execute(sql, (
            eEmail,
            ePhoneNumber,
            eName,
            ePassword,
            eRole,
            image_data,
            employee_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.get("/{employee_id}/profile_image")
async def view_employee_profile_image(employee_id: int):
    """프로필 이미지 조회 (Response - 바이너리 직접 반환)"""
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
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{employee_id}/profile_image")
async def delete_employee_profile_image(employee_id: int):
    """프로필 이미지 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "UPDATE Employee SET eProfileImage=NULL WHERE id=%s"
        curs.execute(sql, (employee_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    """직원 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM Employee WHERE id=%s"
        curs.execute(sql, (employee_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app.api.employees (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Employee API Test")
    test_app.include_router(router, prefix="/api/employees")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)
