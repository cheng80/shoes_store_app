"""
PurchaseItem API
RESTful 기본 CRUD + 복합 쿼리 (JOIN)
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.all_models import PurchaseItem
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_purchase_items(
    pid: Optional[int] = Query(None, description="Product ID로 필터"),
    pcid: Optional[int] = Query(None, description="Purchase ID로 필터"),
    status: Optional[str] = Query(None, description="상태로 필터"),
    order_by: str = Query("id", description="정렬 기준"),
    order: str = Query("asc", description="정렬 방향 (asc, desc)")
):
    """주문 항목 조회 (필터링 및 정렬 가능)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        conditions = []
        params = []
        
        if pid is not None:
            conditions.append("pid = %s")
            params.append(pid)
        if pcid is not None:
            conditions.append("pcid = %s")
            params.append(pcid)
        if status:
            conditions.append("pcStatus = %s")
            params.append(status)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        
        sql = f"""
        SELECT id, pid, pcid, pcQuantity, pcStatus 
        FROM PurchaseItem 
        WHERE {where_clause} 
        ORDER BY {order_by} {order_direction}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pid': row[1],
                'pcid': row[2],
                'pcQuantity': row[3],
                'pcStatus': row[4]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


# ============================================
# 복합 쿼리 (JOIN) - /list/* 엔드포인트 (/{purchase_item_id} 보다 먼저 정의해야 함)
# ============================================

@router.get("/list/with_product")
async def get_purchase_items_list_with_product(pcid: int = Query(..., description="Purchase ID")):
    """주문별 항목 + 제품 정보 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            PurchaseItem.id,
            PurchaseItem.pid,
            PurchaseItem.pcid,
            PurchaseItem.pcQuantity,
            PurchaseItem.pcStatus,
            Product.size,
            Product.basePrice,
            Product.pQuantity,
            Product.pbid,
            Product.mfid
        FROM PurchaseItem
        JOIN Product ON PurchaseItem.pid = Product.id
        WHERE PurchaseItem.pcid = %s
        ORDER BY PurchaseItem.id ASC
        """
        curs.execute(sql, (pcid,))
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pid': row[1],
                'pcid': row[2],
                'pcQuantity': row[3],
                'pcStatus': row[4],
                'size': row[5],
                'basePrice': row[6],
                'pQuantity': row[7],
                'pbid': row[8],
                'mfid': row[9]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/list/full_detail")
async def get_purchase_items_list_full_detail(pcid: int = Query(..., description="Purchase ID")):
    """주문별 항목 전체 상세 정보 조회 (서브쿼리 포함)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            PurchaseItem.id,
            PurchaseItem.pid,
            PurchaseItem.pcid,
            PurchaseItem.pcQuantity,
            PurchaseItem.pcStatus,
            Product.size,
            Product.basePrice,
            Product.pQuantity,
            ProductBase.pName,
            ProductBase.pDescription,
            ProductBase.pColor,
            ProductBase.pGender,
            ProductBase.pCategory,
            ProductBase.pModelNumber,
            Manufacturer.mName,
            (SELECT imagePath FROM ProductImage 
            WHERE ProductImage.pbid = ProductBase.id 
            LIMIT 1) as imagePath
        FROM PurchaseItem
        JOIN Product ON PurchaseItem.pid = Product.id
        JOIN ProductBase ON Product.pbid = ProductBase.id
        JOIN Manufacturer ON Product.mfid = Manufacturer.id
        WHERE PurchaseItem.pcid = %s
        ORDER BY PurchaseItem.id ASC
        """
        curs.execute(sql, (pcid,))
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pid': row[1],
                'pcid': row[2],
                'pcQuantity': row[3],
                'pcStatus': row[4],
                'size': row[5],
                'basePrice': row[6],
                'pQuantity': row[7],
                'pName': row[8],
                'pDescription': row[9],
                'pColor': row[10],
                'pGender': row[11],
                'pCategory': row[12],
                'pModelNumber': row[13],
                'mName': row[14],
                'imagePath': row[15]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{purchase_item_id}")
async def get_purchase_item(purchase_item_id: int):
    """ID로 주문 항목 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, pid, pcid, pcQuantity, pcStatus FROM PurchaseItem WHERE id = %s"
        curs.execute(sql, (purchase_item_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'PurchaseItem not found'}
        
        result = {
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_purchase_item(purchase_item: PurchaseItem):
    """주문 항목 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        INSERT INTO PurchaseItem 
        (pid, pcid, pcQuantity, pcStatus)
        VALUES (%s, %s, %s, %s)
        """
        curs.execute(sql, (
            purchase_item.pid,
            purchase_item.pcid,
            purchase_item.pcQuantity,
            purchase_item.pcStatus
        ))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{purchase_item_id}")
async def update_purchase_item(purchase_item_id: int, purchase_item: PurchaseItem):
    """주문 항목 수정"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        UPDATE PurchaseItem
        SET pid=%s, pcid=%s, pcQuantity=%s, pcStatus=%s
        WHERE id=%s
        """
        curs.execute(sql, (
            purchase_item.pid,
            purchase_item.pcid,
            purchase_item.pcQuantity,
            purchase_item.pcStatus,
            purchase_item_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{purchase_item_id}")
async def delete_purchase_item(purchase_item_id: int):
    """주문 항목 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM PurchaseItem WHERE id=%s"
        curs.execute(sql, (purchase_item_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


# ============================================
# 복합 쿼리 (JOIN) - /{id}/* 엔드포인트
# ============================================

@router.get("/{purchase_item_id}/with_product")
async def get_purchase_item_with_product(purchase_item_id: int):
    """주문 항목 + 제품 정보 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            PurchaseItem.*,
            Product.size,
            Product.basePrice,
            Product.pQuantity,
            Product.pbid,
            Product.mfid
        FROM PurchaseItem
        JOIN Product ON PurchaseItem.pid = Product.id
        WHERE PurchaseItem.id = %s
        """
        curs.execute(sql, (purchase_item_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'PurchaseItem not found'}
        
        result = {
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4],
            'size': row[5],
            'basePrice': row[6],
            'pQuantity': row[7],
            'pbid': row[8],
            'mfid': row[9]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{purchase_item_id}/full_detail")
async def get_purchase_item_full_detail(purchase_item_id: int):
    """주문 항목 전체 상세 정보 조회 (4개 테이블 JOIN)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            PurchaseItem.*,
            Product.size,
            Product.basePrice,
            Product.pQuantity,
            ProductBase.pName,
            ProductBase.pDescription,
            ProductBase.pColor,
            ProductBase.pGender,
            ProductBase.pCategory,
            ProductBase.pModelNumber,
            Manufacturer.mName,
            ProductImage.imagePath
        FROM PurchaseItem
        JOIN Product ON PurchaseItem.pid = Product.id
        JOIN ProductBase ON Product.pbid = ProductBase.id
        JOIN Manufacturer ON Product.mfid = Manufacturer.id
        LEFT JOIN ProductImage ON ProductBase.id = ProductImage.pbid
        WHERE PurchaseItem.id = %s
        LIMIT 1
        """
        curs.execute(sql, (purchase_item_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'PurchaseItem not found'}
        
        result = {
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4],
            'size': row[5],
            'basePrice': row[6],
            'pQuantity': row[7],
            'pName': row[8],
            'pDescription': row[9],
            'pColor': row[10],
            'pGender': row[11],
            'pCategory': row[12],
            'pModelNumber': row[13],
            'mName': row[14],
            'imagePath': row[15]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app.api.purchase_items (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="PurchaseItem API Test")
    test_app.include_router(router, prefix="/api/purchase_items")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)
