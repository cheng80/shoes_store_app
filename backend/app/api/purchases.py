"""
Purchase API
RESTful 기본 CRUD + 복합 쿼리 (JOIN)
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.all_models import Purchase
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_purchases(
    cid: Optional[int] = Query(None, description="Customer ID로 필터"),
    order_code: Optional[str] = Query(None, description="주문 코드로 필터"),
    order_by: str = Query("timeStamp", description="정렬 기준"),
    order: str = Query("desc", description="정렬 방향 (asc, desc)")
):
    """주문 조회 (필터링 및 정렬 가능)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        conditions = []
        params = []
        
        if cid is not None:
            conditions.append("cid = %s")
            params.append(cid)
        if order_code:
            conditions.append("orderCode = %s")
            params.append(order_code)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        
        sql = f"""
        SELECT id, cid, pickupDate, orderCode, timeStamp 
        FROM Purchase 
        WHERE {where_clause} 
        ORDER BY {order_by} {order_direction}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'cid': row[1],
                'pickupDate': row[2],
                'orderCode': row[3],
                'timeStamp': row[4]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{purchase_id}")
async def get_purchase(purchase_id: int):
    """ID로 주문 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, cid, pickupDate, orderCode, timeStamp FROM Purchase WHERE id = %s"
        curs.execute(sql, (purchase_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Purchase not found'}
        
        result = {
            'id': row[0],
            'cid': row[1],
            'pickupDate': row[2],
            'orderCode': row[3],
            'timeStamp': row[4]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_purchase(purchase: Purchase):
    """주문 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        if purchase.cid is None:
            return {"result": "Error", "message": "cid is required"}
        
        sql = """
        INSERT INTO Purchase 
        (cid, pickupDate, orderCode, timeStamp)
        VALUES (%s, %s, %s, %s)
        """
        curs.execute(sql, (
            purchase.cid,
            purchase.pickupDate,
            purchase.orderCode,
            purchase.timeStamp
        ))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{purchase_id}")
async def update_purchase(purchase_id: int, purchase: Purchase):
    """주문 수정"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        UPDATE Purchase
        SET cid=%s, pickupDate=%s, orderCode=%s, timeStamp=%s
        WHERE id=%s
        """
        curs.execute(sql, (
            purchase.cid,
            purchase.pickupDate,
            purchase.orderCode,
            purchase.timeStamp,
            purchase_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{purchase_id}")
async def delete_purchase(purchase_id: int):
    """주문 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM Purchase WHERE id=%s"
        curs.execute(sql, (purchase_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


# ============================================
# 복합 쿼리 (JOIN) - 별도 엔드포인트
# ============================================

@router.get("/{purchase_id}/with_customer")
async def get_purchase_with_customer(purchase_id: int):
    """주문 + 고객 정보 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            Purchase.*,
            Customer.cName,
            Customer.cEmail,
            Customer.cPhoneNumber
        FROM Purchase
        JOIN Customer ON Purchase.cid = Customer.id
        WHERE Purchase.id = %s
        """
        curs.execute(sql, (purchase_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Purchase not found'}
        
        result = {
            'id': row[0],
            'cid': row[1],
            'pickupDate': row[2],
            'orderCode': row[3],
            'timeStamp': row[4],
            'cName': row[5],
            'cEmail': row[6],
            'cPhoneNumber': row[7]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/list/with_customer")
async def get_purchases_list_with_customer(cid: int = Query(..., description="Customer ID")):
    """고객별 주문 목록 + 고객 정보 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            Purchase.*,
            Customer.cName,
            Customer.cEmail,
            Customer.cPhoneNumber
        FROM Purchase
        JOIN Customer ON Purchase.cid = Customer.id
        WHERE Purchase.cid = %s
        ORDER BY Purchase.timeStamp DESC
        """
        curs.execute(sql, (cid,))
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'cid': row[1],
                'pickupDate': row[2],
                'orderCode': row[3],
                'timeStamp': row[4],
                'cName': row[5],
                'cEmail': row[6],
                'cPhoneNumber': row[7]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()
