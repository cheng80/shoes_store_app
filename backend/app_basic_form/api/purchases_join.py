"""
Purchase 복합 쿼리 API (JOIN)
- Purchase 중심의 JOIN 쿼리들
- Purchase + Customer + PurchaseItem
"""

from fastapi import APIRouter, Query
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# Purchase + Customer
# ============================================
@router.get("/{purchase_id}/with_customer")
async def get_purchase_with_customer(purchase_id: int):
    """
    특정 Purchase + Customer 정보
    JOIN: Purchase + Customer
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pc.id,
            pc.cid,
            pc.pickupDate,
            pc.orderCode,
            pc.timeStamp,
            c.cName,
            c.cEmail,
            c.cPhoneNumber
        FROM Purchase pc
        JOIN Customer c ON pc.cid = c.id
        WHERE pc.id = %s
        """
        curs.execute(sql, (purchase_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Purchase not found"}
        
        result = {
            'id': row[0],
            'cid': row[1],
            'pickupDate': str(row[2]) if row[2] else None,
            'orderCode': row[3],
            'timeStamp': str(row[4]) if row[4] else None,
            'customer': {
                'cName': row[5],
                'cEmail': row[6],
                'cPhoneNumber': row[7]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Purchase 목록 + Customer (고객별 또는 전체)
# ============================================
@router.get("/with_customer")
async def get_purchases_with_customer(cid: Optional[int] = Query(None, description="고객 ID (없으면 전체)")):
    """
    Purchase 목록 + Customer 정보
    JOIN: Purchase + Customer
    용도: 주문 목록 화면 (고객별 또는 관리자용 전체)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        if cid:
            sql = """
            SELECT 
                pc.id,
                pc.cid,
                pc.pickupDate,
                pc.orderCode,
                pc.timeStamp,
                c.cName,
                c.cEmail,
                c.cPhoneNumber
            FROM Purchase pc
            JOIN Customer c ON pc.cid = c.id
            WHERE pc.cid = %s
            ORDER BY pc.id DESC
            """
            curs.execute(sql, (cid,))
        else:
            sql = """
            SELECT 
                pc.id,
                pc.cid,
                pc.pickupDate,
                pc.orderCode,
                pc.timeStamp,
                c.cName,
                c.cEmail,
                c.cPhoneNumber
            FROM Purchase pc
            JOIN Customer c ON pc.cid = c.id
            ORDER BY pc.id DESC
            """
            curs.execute(sql)
        
        rows = curs.fetchall()
        
        result = [{
            'id': row[0],
            'cid': row[1],
            'pickupDate': str(row[2]) if row[2] else None,
            'orderCode': row[3],
            'timeStamp': str(row[4]) if row[4] else None,
            'customer': {
                'cName': row[5],
                'cEmail': row[6],
                'cPhoneNumber': row[7]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Purchase + PurchaseItem 목록
# ============================================
@router.get("/{purchase_id}/with_items")
async def get_purchase_with_items(purchase_id: int):
    """
    특정 Purchase + 주문 항목 목록
    JOIN: Purchase + PurchaseItem
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # Purchase 정보 조회
        sql_purchase = """
        SELECT id, cid, pickupDate, orderCode, timeStamp
        FROM Purchase
        WHERE id = %s
        """
        curs.execute(sql_purchase, (purchase_id,))
        purchase_row = curs.fetchone()
        
        if purchase_row is None:
            return {"result": "Error", "message": "Purchase not found"}
        
        # PurchaseItem 목록 조회
        sql_items = """
        SELECT id, pid, pcid, pcQuantity, pcStatus
        FROM PurchaseItem
        WHERE pcid = %s
        ORDER BY id
        """
        curs.execute(sql_items, (purchase_id,))
        item_rows = curs.fetchall()
        
        result = {
            'id': purchase_row[0],
            'cid': purchase_row[1],
            'pickupDate': str(purchase_row[2]) if purchase_row[2] else None,
            'orderCode': purchase_row[3],
            'timeStamp': str(purchase_row[4]) if purchase_row[4] else None,
            'items': [{
                'id': row[0],
                'pid': row[1],
                'pcid': row[2],
                'pcQuantity': row[3],
                'pcStatus': row[4]
            } for row in item_rows],
            'itemCount': len(item_rows)
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Purchase 목록 + PurchaseItem 목록 (고객별 또는 전체)
# ============================================
@router.get("/with_items")
async def get_purchases_with_items(cid: Optional[int] = Query(None, description="고객 ID (없으면 전체)")):
    """
    Purchase 목록 + 각 주문의 항목 목록
    JOIN: Purchase + PurchaseItem
    용도: 주문 목록 화면
    
    🚀 최적화 API: Purchase 조회 후 각각 PurchaseItem 조회하던 것을 1번으로!
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # Purchase 목록 조회
        if cid:
            sql_purchases = """
            SELECT id, cid, pickupDate, orderCode, timeStamp
            FROM Purchase
            WHERE cid = %s
            ORDER BY id DESC
            """
            curs.execute(sql_purchases, (cid,))
        else:
            sql_purchases = """
            SELECT id, cid, pickupDate, orderCode, timeStamp
            FROM Purchase
            ORDER BY id DESC
            """
            curs.execute(sql_purchases)
        
        purchase_rows = curs.fetchall()
        
        result = []
        for p_row in purchase_rows:
            purchase_id = p_row[0]
            
            # 각 Purchase의 PurchaseItem 조회
            sql_items = """
            SELECT id, pid, pcid, pcQuantity, pcStatus
            FROM PurchaseItem
            WHERE pcid = %s
            ORDER BY id
            """
            curs.execute(sql_items, (purchase_id,))
            item_rows = curs.fetchall()
            
            purchase = {
                'id': p_row[0],
                'cid': p_row[1],
                'pickupDate': str(p_row[2]) if p_row[2] else None,
                'orderCode': p_row[3],
                'timeStamp': str(p_row[4]) if p_row[4] else None,
                'items': [{
                    'id': row[0],
                    'pid': row[1],
                    'pcid': row[2],
                    'pcQuantity': row[3],
                    'pcStatus': row[4]
                } for row in item_rows],
                'itemCount': len(item_rows)
            }
            result.append(purchase)
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Purchase 전체 상세 (Customer + Items)
# ============================================
@router.get("/{purchase_id}/full_detail")
async def get_purchase_full_detail(purchase_id: int):
    """
    특정 Purchase의 전체 상세 정보
    JOIN: Purchase + Customer + PurchaseItem
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # Purchase + Customer 조회
        sql = """
        SELECT 
            pc.id,
            pc.cid,
            pc.pickupDate,
            pc.orderCode,
            pc.timeStamp,
            c.cName,
            c.cEmail,
            c.cPhoneNumber
        FROM Purchase pc
        JOIN Customer c ON pc.cid = c.id
        WHERE pc.id = %s
        """
        curs.execute(sql, (purchase_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Purchase not found"}
        
        # PurchaseItem 목록 조회
        sql_items = """
        SELECT id, pid, pcid, pcQuantity, pcStatus
        FROM PurchaseItem
        WHERE pcid = %s
        ORDER BY id
        """
        curs.execute(sql_items, (purchase_id,))
        item_rows = curs.fetchall()
        
        result = {
            'id': row[0],
            'cid': row[1],
            'pickupDate': str(row[2]) if row[2] else None,
            'orderCode': row[3],
            'timeStamp': str(row[4]) if row[4] else None,
            'customer': {
                'cName': row[5],
                'cEmail': row[6],
                'cPhoneNumber': row[7]
            },
            'items': [{
                'id': item[0],
                'pid': item[1],
                'pcid': item[2],
                'pcQuantity': item[3],
                'pcStatus': item[4]
            } for item in item_rows],
            'itemCount': len(item_rows)
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.purchases_join (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Purchase JOIN API Test")
    test_app.include_router(router, prefix="/api/purchases")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

