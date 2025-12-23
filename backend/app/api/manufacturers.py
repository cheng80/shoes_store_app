"""
Manufacturer API
RESTful 기본 CRUD
"""

from fastapi import APIRouter
from app.models.all_models import Manufacturer
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_manufacturers():
    """모든 제조사 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, mName FROM Manufacturer ORDER BY id ASC"
        curs.execute(sql)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'mName': row[1]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{manufacturer_id}")
async def get_manufacturer(manufacturer_id: int):
    """ID로 제조사 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, mName FROM Manufacturer WHERE id = %s"
        curs.execute(sql, (manufacturer_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Manufacturer not found'}
        
        result = {
            'id': row[0],
            'mName': row[1]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_manufacturer(manufacturer: Manufacturer):
    """제조사 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "INSERT INTO Manufacturer (mName) VALUES (%s)"
        curs.execute(sql, (manufacturer.mName,))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{manufacturer_id}")
async def update_manufacturer(manufacturer_id: int, manufacturer: Manufacturer):
    """제조사 수정"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "UPDATE Manufacturer SET mName=%s WHERE id=%s"
        curs.execute(sql, (manufacturer.mName, manufacturer_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{manufacturer_id}")
async def delete_manufacturer(manufacturer_id: int):
    """제조사 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM Manufacturer WHERE id=%s"
        curs.execute(sql, (manufacturer_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()
