"""
Customer API
RESTful 기본 CRUD + 필터링 + 프로필 이미지

Note: INSERT는 이미지 포함 필수, UPDATE는 이미지 제외/포함 두 가지 방식 제공
"""

from fastapi import APIRouter, Query, UploadFile, File, Response, Form
from typing import Optional
from app.models.all_models import Customer
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_customers(
    email: Optional[str] = Query(None, description="이메일로 필터"),
    phone: Optional[str] = Query(None, description="전화번호로 필터"),
    identifier: Optional[str] = Query(None, description="이메일 또는 전화번호로 필터 (OR 조건)"),
    order_by: str = Query("id", description="정렬 기준"),
    order: str = Query("asc", description="정렬 방향 (asc, desc)")
):
    """고객 조회 (필터링 및 정렬 가능, 이미지 제외)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        conditions = []
        params = []
        
        if identifier:
            # 이메일 또는 전화번호로 검색 (OR 조건)
            conditions.append("(cEmail = %s OR cPhoneNumber = %s)")
            params.extend([identifier, identifier])
        else:
            if email:
                conditions.append("cEmail = %s")
                params.append(email)
            if phone:
                conditions.append("cPhoneNumber = %s")
                params.append(phone)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        
        sql = f"""
        SELECT id, cEmail, cPhoneNumber, cName, cPassword 
        FROM Customer 
        WHERE {where_clause} 
        ORDER BY {order_by} {order_direction}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'cEmail': row[1],
                'cPhoneNumber': row[2],
                'cName': row[3],
                'cPassword': row[4]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{customer_id}")
async def get_customer(customer_id: int):
    """ID로 고객 조회 (이미지 제외)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, cEmail, cPhoneNumber, cName, cPassword FROM Customer WHERE id = %s"
        curs.execute(sql, (customer_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Customer not found'}
        
        result = {
            'id': row[0],
            'cEmail': row[1],
            'cPhoneNumber': row[2],
            'cName': row[3],
            'cPassword': row[4]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_customer(
    cEmail: str = Form(...),
    cPhoneNumber: str = Form(...),
    cName: str = Form(...),
    cPassword: str = Form(...),
    file: UploadFile = File(...)
):
    """고객 생성 (이미지 포함 필수)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 파일 읽기
        image_data = await file.read()
        
        sql = """
        INSERT INTO Customer 
        (cEmail, cPhoneNumber, cName, cPassword, cProfileImage)
        VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (
            cEmail,
            cPhoneNumber,
            cName,
            cPassword,
            image_data
        ))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    """고객 수정 (이미지 제외)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        UPDATE Customer
        SET cEmail=%s, cPhoneNumber=%s, cName=%s, cPassword=%s
        WHERE id=%s
        """
        curs.execute(sql, (
            customer.cEmail,
            customer.cPhoneNumber,
            customer.cName,
            customer.cPassword,
            customer_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.post("/{customer_id}/with_image")
async def update_customer_with_image(
    customer_id: int,
    cEmail: str = Form(...),
    cPhoneNumber: str = Form(...),
    cName: str = Form(...),
    cPassword: str = Form(...),
    file: UploadFile = File(...)
):
    """고객 수정 (이미지 포함)"""
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
        curs.execute(sql, (
            cEmail,
            cPhoneNumber,
            cName,
            cPassword,
            image_data,
            customer_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.get("/{customer_id}/profile_image")
async def view_customer_profile_image(customer_id: int):
    """프로필 이미지 조회 (Response - 바이너리 직접 반환)"""
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
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{customer_id}/profile_image")
async def delete_customer_profile_image(customer_id: int):
    """프로필 이미지 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "UPDATE Customer SET cProfileImage=NULL WHERE id=%s"
        curs.execute(sql, (customer_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int):
    """고객 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM Customer WHERE id=%s"
        curs.execute(sql, (customer_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app.api.customers (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Customer API Test")
    test_app.include_router(router, prefix="/api/customers")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)
