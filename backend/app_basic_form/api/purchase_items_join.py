"""
PurchaseItem 복합 쿼리 API (JOIN)
- PurchaseItem 중심의 JOIN 쿼리들
- PurchaseItem + Product + ProductBase + Manufacturer
"""

from fastapi import APIRouter
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# PurchaseItem + Product
# ============================================
@router.get("/{item_id}/with_product")
async def get_purchase_item_with_product(item_id: int):
    """
    특정 PurchaseItem + Product 정보
    JOIN: PurchaseItem + Product
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pi.id,
            pi.pid,
            pi.pcid,
            pi.pcQuantity,
            pi.pcStatus,
            p.pbid,
            p.mfid,
            p.size,
            p.basePrice,
            p.pQuantity as stock
        FROM PurchaseItem pi
        JOIN Product p ON pi.pid = p.id
        WHERE pi.id = %s
        """
        curs.execute(sql, (item_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "PurchaseItem not found"}
        
        result = {
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4],
            'product': {
                'id': row[1],
                'pbid': row[5],
                'mfid': row[6],
                'size': row[7],
                'basePrice': row[8],
                'stock': row[9]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# PurchaseItem 목록 + Product (주문별)
# ============================================
@router.get("/by_pcid/{pcid}/with_product")
async def get_purchase_items_by_pcid_with_product(pcid: int):
    """
    특정 Purchase의 모든 PurchaseItem + Product 정보
    JOIN: PurchaseItem + Product
    용도: 주문 상세 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pi.id,
            pi.pid,
            pi.pcid,
            pi.pcQuantity,
            pi.pcStatus,
            p.pbid,
            p.size,
            p.basePrice
        FROM PurchaseItem pi
        JOIN Product p ON pi.pid = p.id
        WHERE pi.pcid = %s
        ORDER BY pi.id
        """
        curs.execute(sql, (pcid,))
        rows = curs.fetchall()
        
        result = [{
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4],
            'product': {
                'id': row[1],
                'pbid': row[5],
                'size': row[6],
                'basePrice': row[7]
            }
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# PurchaseItem 전체 상세 (4테이블 JOIN)
# ============================================
@router.get("/{item_id}/full_detail")
async def get_purchase_item_full_detail(item_id: int):
    """
    특정 PurchaseItem의 전체 상세 정보
    JOIN: PurchaseItem + Product + ProductBase + Manufacturer (4테이블)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pi.id,
            pi.pid,
            pi.pcid,
            pi.pcQuantity,
            pi.pcStatus,
            p.size,
            p.basePrice,
            pb.id as pb_id,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pCategory,
            m.id as m_id,
            m.mName
        FROM PurchaseItem pi
        JOIN Product p ON pi.pid = p.id
        JOIN ProductBase pb ON p.pbid = pb.id
        JOIN Manufacturer m ON p.mfid = m.id
        WHERE pi.id = %s
        """
        curs.execute(sql, (item_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "PurchaseItem not found"}
        
        result = {
            'id': row[0],
            'pid': row[1],
            'pcid': row[2],
            'pcQuantity': row[3],
            'pcStatus': row[4],
            'size': row[5],
            'basePrice': row[6],
            'productBase': {
                'id': row[7],
                'pName': row[8],
                'pDescription': row[9],
                'pColor': row[10],
                'pCategory': row[11]
            },
            'manufacturer': {
                'id': row[12],
                'mName': row[13]
            },
            # 계산된 값
            'totalPrice': row[6] * row[3]  # basePrice * pcQuantity
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# PurchaseItem 목록 전체 상세 (주문별)
# ============================================
@router.get("/by_pcid/{pcid}/full_detail")
async def get_purchase_items_by_pcid_full_detail(pcid: int):
    """
    특정 Purchase의 모든 PurchaseItem 전체 상세 정보
    JOIN: PurchaseItem + Product + ProductBase + Manufacturer (4테이블)
    용도: 주문 상세 화면에서 상품명, 브랜드 등 표시
    
    🚀 최적화 API: 주문 항목별로 여러 번 조회하던 것을 1번으로!
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pi.id,
            pi.pid,
            pi.pcid,
            pi.pcQuantity,
            pi.pcStatus,
            p.size,
            p.basePrice,
            pb.id as pb_id,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pCategory,
            m.id as m_id,
            m.mName,
            (SELECT imagePath FROM ProductImage WHERE pbid = pb.id LIMIT 1) as firstImage
        FROM PurchaseItem pi
        JOIN Product p ON pi.pid = p.id
        JOIN ProductBase pb ON p.pbid = pb.id
        JOIN Manufacturer m ON p.mfid = m.id
        WHERE pi.pcid = %s
        ORDER BY pi.id
        """
        curs.execute(sql, (pcid,))
        rows = curs.fetchall()
        
        result = []
        total_amount = 0
        
        for row in rows:
            item_total = row[6] * row[3]  # basePrice * pcQuantity
            total_amount += item_total
            
            result.append({
                'id': row[0],
                'pid': row[1],
                'pcid': row[2],
                'pcQuantity': row[3],
                'pcStatus': row[4],
                'size': row[5],
                'basePrice': row[6],
                'productBase': {
                    'id': row[7],
                    'pName': row[8],
                    'pDescription': row[9],
                    'pColor': row[10],
                    'pCategory': row[11]
                },
                'manufacturer': {
                    'id': row[12],
                    'mName': row[13]
                },
                'firstImage': row[14],
                'itemTotal': item_total
            })
        
        return {
            "results": result,
            "totalAmount": total_amount,
            "itemCount": len(result)
        }
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 주문 요약 정보 (집계)
# ============================================
@router.get("/summary/{pcid}")
async def get_purchase_items_summary(pcid: int):
    """
    특정 Purchase의 주문 요약 정보
    - 총 상품 수, 총 금액, 상태별 개수
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 총 수량 및 금액
        sql_total = """
        SELECT 
            COUNT(*) as itemCount,
            SUM(pi.pcQuantity) as totalQuantity,
            SUM(p.basePrice * pi.pcQuantity) as totalAmount
        FROM PurchaseItem pi
        JOIN Product p ON pi.pid = p.id
        WHERE pi.pcid = %s
        """
        curs.execute(sql_total, (pcid,))
        total_row = curs.fetchone()
        
        # 상태별 개수
        sql_status = """
        SELECT pcStatus, COUNT(*) as count
        FROM PurchaseItem
        WHERE pcid = %s
        GROUP BY pcStatus
        """
        curs.execute(sql_status, (pcid,))
        status_rows = curs.fetchall()
        
        result = {
            'pcid': pcid,
            'itemCount': total_row[0] or 0,
            'totalQuantity': total_row[1] or 0,
            'totalAmount': total_row[2] or 0,
            'statusSummary': {row[0]: row[1] for row in status_rows}
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.purchase_items_join (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="PurchaseItem JOIN API Test")
    test_app.include_router(router, prefix="/api/purchase_items")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

