"""
Product API
RESTful 기본 CRUD + 복합 쿼리 (JOIN)
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.all_models import Product
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_products(
    pbid: Optional[int] = Query(None, description="ProductBase ID로 필터"),
    mfid: Optional[int] = Query(None, description="Manufacturer ID로 필터"),
    size: Optional[int] = Query(None, description="사이즈로 필터"),
    order_by: str = Query("id", description="정렬 기준 (id, size, basePrice, pQuantity)"),
    order: str = Query("asc", description="정렬 방향 (asc, desc)")
):
    """제품 조회 (필터링 및 정렬 가능)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # WHERE 조건 동적 생성
        conditions = []
        params = []
        
        if pbid is not None:
            conditions.append("pbid = %s")
            params.append(pbid)
        if mfid is not None:
            conditions.append("mfid = %s")
            params.append(mfid)
        if size is not None:
            conditions.append("size = %s")
            params.append(size)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        
        # ORDER BY 검증
        valid_order_by = ["id", "size", "basePrice", "pQuantity"]
        if order_by not in valid_order_by:
            order_by = "id"
        
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        order_clause = f"ORDER BY {order_by} {order_direction}"
        
        sql = f"""
        SELECT id, pbid, mfid, size, basePrice, pQuantity 
        FROM Product 
        WHERE {where_clause} 
        {order_clause}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pbid': row[1],
                'mfid': row[2],
                'size': row[3],
                'basePrice': row[4],
                'pQuantity': row[5]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{product_id}")
async def get_product(product_id: int):
    """ID로 제품 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "SELECT id, pbid, mfid, size, basePrice, pQuantity FROM Product WHERE id = %s"
        curs.execute(sql, (product_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Product not found'}
        
        result = {
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_product(product: Product):
    """제품 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        if product.pbid is None or product.mfid is None:
            return {"result": "Error", "message": "pbid and mfid are required"}
        
        sql = """
        INSERT INTO Product 
        (pbid, mfid, size, basePrice, pQuantity)
        VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (
            product.pbid,
            product.mfid,
            product.size,
            product.basePrice,
            product.pQuantity
        ))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{product_id}")
async def update_product(product_id: int, product: Product):
    """제품 수정"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        UPDATE Product
        SET pbid=%s, mfid=%s, size=%s, basePrice=%s, pQuantity=%s
        WHERE id=%s
        """
        curs.execute(sql, (
            product.pbid,
            product.mfid,
            product.size,
            product.basePrice,
            product.pQuantity,
            product_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """제품 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM Product WHERE id=%s"
        curs.execute(sql, (product_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


# ============================================
# 복합 쿼리 (JOIN) - 별도 엔드포인트
# ============================================

@router.get("/{product_id}/with_base")
async def get_product_with_base(product_id: int):
    """제품 + ProductBase 정보 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            Product.*,
            ProductBase.pName,
            ProductBase.pDescription,
            ProductBase.pColor,
            ProductBase.pGender,
            ProductBase.pStatus,
            ProductBase.pCategory,
            ProductBase.pModelNumber
        FROM Product
        JOIN ProductBase ON Product.pbid = ProductBase.id
        WHERE Product.id = %s
        """
        curs.execute(sql, (product_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Product not found'}
        
        result = {
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5],
            'pName': row[6],
            'pDescription': row[7],
            'pColor': row[8],
            'pGender': row[9],
            'pStatus': row[10],
            'pCategory': row[11],
            'pModelNumber': row[12]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{product_id}/with_base_and_manufacturer")
async def get_product_with_base_and_manufacturer(product_id: int):
    """제품 + ProductBase + Manufacturer 정보 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            Product.*,
            ProductBase.pName,
            ProductBase.pDescription,
            ProductBase.pColor,
            ProductBase.pGender,
            ProductBase.pStatus,
            ProductBase.pCategory,
            ProductBase.pModelNumber,
            Manufacturer.mName
        FROM Product
        JOIN ProductBase ON Product.pbid = ProductBase.id
        JOIN Manufacturer ON Product.mfid = Manufacturer.id
        WHERE Product.id = %s
        """
        curs.execute(sql, (product_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'Product not found'}
        
        result = {
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5],
            'pName': row[6],
            'pDescription': row[7],
            'pColor': row[8],
            'pGender': row[9],
            'pStatus': row[10],
            'pCategory': row[11],
            'pModelNumber': row[12],
            'mName': row[13]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/list/with_base")
async def get_products_list_with_base(pbid: int = Query(..., description="ProductBase ID")):
    """ProductBase별 제품 목록 + ProductBase 정보 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            Product.*,
            ProductBase.pName,
            ProductBase.pDescription,
            ProductBase.pColor,
            ProductBase.pGender,
            ProductBase.pStatus,
            ProductBase.pCategory,
            ProductBase.pModelNumber
        FROM Product
        JOIN ProductBase ON Product.pbid = ProductBase.id
        WHERE Product.pbid = %s
        ORDER BY Product.size ASC
        """
        curs.execute(sql, (pbid,))
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pbid': row[1],
                'mfid': row[2],
                'size': row[3],
                'basePrice': row[4],
                'pQuantity': row[5],
                'pName': row[6],
                'pDescription': row[7],
                'pColor': row[8],
                'pGender': row[9],
                'pStatus': row[10],
                'pCategory': row[11],
                'pModelNumber': row[12]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()
