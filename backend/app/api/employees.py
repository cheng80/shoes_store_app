"""
Employee API
RESTful 기본 CRUD
"""

from fastapi import APIRouter
from app.models.all_models import Employee
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_employees():
    """모든 직원 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, eEmail, ePhoneNumber, eName, ePassword, eRole FROM Employee ORDER BY id ASC"
        curs.execute(sql)
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
