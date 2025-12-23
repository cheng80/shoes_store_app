"""
LoginHistory API
RESTful 기본 CRUD
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.all_models import LoginHistory
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_login_histories(
    cid: Optional[int] = Query(None, description="Customer ID로 필터"),
    order_by: str = Query("id", description="정렬 기준"),
    order: str = Query("desc", description="정렬 방향 (asc, desc)")
):
    """로그인 이력 조회 (필터링 및 정렬 가능)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        conditions = []
        params = []
        
        if cid is not None:
            conditions.append("cid = %s")
            params.append(cid)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        
        sql = f"""
        SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
        FROM LoginHistory 
        WHERE {where_clause} 
        ORDER BY {order_by} {order_direction}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'cid': row[1],
                'loginTime': row[2],
                'lStatus': row[3],
                'lVersion': row[4],
                'lAddress': row[5],
                'lPaymentMethod': row[6]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{login_history_id}")
async def get_login_history(login_history_id: int):
    """ID로 로그인 이력 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT id, cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod 
        FROM LoginHistory WHERE id = %s
        """
        curs.execute(sql, (login_history_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'LoginHistory not found'}
        
        result = {
            'id': row[0],
            'cid': row[1],
            'loginTime': row[2],
            'lStatus': row[3],
            'lVersion': row[4],
            'lAddress': row[5],
            'lPaymentMethod': row[6]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_login_history(login_history: LoginHistory):
    """로그인 이력 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        if login_history.cid is None:
            return {"result": "Error", "message": "cid is required"}
        
        sql = """
        INSERT INTO LoginHistory 
        (cid, loginTime, lStatus, lVersion, lAddress, lPaymentMethod)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (
            login_history.cid,
            login_history.loginTime,
            login_history.lStatus,
            login_history.lVersion,
            login_history.lAddress,
            login_history.lPaymentMethod
        ))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{login_history_id}")
async def update_login_history(login_history_id: int, login_history: LoginHistory):
    """로그인 이력 수정"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        UPDATE LoginHistory
        SET cid=%s, loginTime=%s, lStatus=%s, lVersion=%s, lAddress=%s, lPaymentMethod=%s
        WHERE id=%s
        """
        curs.execute(sql, (
            login_history.cid,
            login_history.loginTime,
            login_history.lStatus,
            login_history.lVersion,
            login_history.lAddress,
            login_history.lPaymentMethod,
            login_history_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{login_history_id}")
async def delete_login_history(login_history_id: int):
    """로그인 이력 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM LoginHistory WHERE id=%s"
        curs.execute(sql, (login_history_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()
