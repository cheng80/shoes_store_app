"""
Employee API
RESTful 기본 CRUD + 필터링
"""

from fastapi import APIRouter, Query
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
    """직원 조회 (필터링 및 정렬 가능)"""
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
    """ID로 직원 조회"""
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
async def create_employee(employee: Employee):
    """직원 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        INSERT INTO Employee 
        (eEmail, ePhoneNumber, eName, ePassword, eRole)
        VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (
            employee.eEmail,
            employee.ePhoneNumber,
            employee.eName,
            employee.ePassword,
            employee.eRole
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
    """직원 수정"""
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
