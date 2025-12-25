"""
ProductBase API
RESTful 기본 CRUD + 복합 쿼리
"""

from fastapi import APIRouter, Query
from typing import Optional
from app.models.all_models import ProductBase
from app.database.connection import connect_db

router = APIRouter()


@router.get("")
async def get_product_bases(
    name: Optional[str] = Query(None, description="이름으로 필터"),
    color: Optional[str] = Query(None, description="색상으로 필터"),
    category: Optional[str] = Query(None, description="카테고리로 필터"),
    order_by: str = Query("id", description="정렬 기준"),
    order: str = Query("asc", description="정렬 방향 (asc, desc)")
):
    """ProductBase 조회 (필터링 및 정렬 가능)"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        conditions = []
        params = []
        
        if name:
            conditions.append("pName = %s")
            params.append(name)
        if color:
            conditions.append("pColor = %s")
            params.append(color)
        if category:
            conditions.append("pCategory = %s")
            params.append(category)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        order_direction = "DESC" if order.lower() == "desc" else "ASC"
        
        sql = f"""
        SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
        FROM ProductBase 
        WHERE {where_clause} 
        ORDER BY {order_by} {order_direction}
        """
        curs.execute(sql, params)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pName': row[1],
                'pDescription': row[2],
                'pColor': row[3],
                'pGender': row[4],
                'pStatus': row[5],
                'pCategory': row[6],
                'pModelNumber': row[7]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


# ============================================
# 복합 쿼리 - /list/* 엔드포인트 (/{id} 보다 먼저 정의해야 함)
# ============================================

@router.get("/list/with_first_image")
async def get_product_bases_list_with_first_image():
    """ProductBase 목록 + 첫 번째 이미지 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            ProductBase.id,
            ProductBase.pName,
            ProductBase.pDescription,
            ProductBase.pColor,
            ProductBase.pGender,
            ProductBase.pStatus,
            ProductBase.pCategory,
            ProductBase.pModelNumber,
            (SELECT imagePath FROM ProductImage 
             WHERE ProductImage.pbid = ProductBase.id 
             LIMIT 1) as firstImage
        FROM ProductBase
        ORDER BY ProductBase.id ASC
        """
        curs.execute(sql)
        rows = curs.fetchall()
        
        result = [
            {
                'id': row[0],
                'pName': row[1],
                'pDescription': row[2],
                'pColor': row[3],
                'pGender': row[4],
                'pStatus': row[5],
                'pCategory': row[6],
                'pModelNumber': row[7],
                'firstImage': row[8]
            }
            for row in rows
        ]
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/list/full_detail")
async def get_product_bases_list_full_detail():
    """
    ProductBase 전체 상세 목록 (검색 화면용)
    ProductBase + 첫 번째 이미지 + 대표 Product(첫번째) + Manufacturer 통합 조회
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 복잡한 조인을 한번에 처리
        sql = """
        SELECT 
            pb.id AS pb_id,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pStatus,
            pb.pCategory,
            pb.pModelNumber,
            (SELECT imagePath FROM ProductImage 
             WHERE ProductImage.pbid = pb.id 
             LIMIT 1) AS firstImage,
            p.id AS product_id,
            p.size,
            p.basePrice,
            p.discountRate,
            p.stock,
            m.id AS manufacturer_id,
            m.mName AS manufacturerName,
            m.mDescription AS manufacturerDescription
        FROM ProductBase pb
        LEFT JOIN Product p ON p.pbid = pb.id AND p.id = (
            SELECT MIN(id) FROM Product WHERE pbid = pb.id
        )
        LEFT JOIN Manufacturer m ON p.mfid = m.id
        ORDER BY pb.id ASC
        """
        curs.execute(sql)
        rows = curs.fetchall()
        
        result = []
        for row in rows:
            item = {
                'id': row[0],
                'pName': row[1],
                'pDescription': row[2],
                'pColor': row[3],
                'pGender': row[4],
                'pStatus': row[5],
                'pCategory': row[6],
                'pModelNumber': row[7],
                'firstImage': row[8],
                'representativeProduct': None,
                'manufacturer': None
            }
            
            # 대표 Product 정보
            if row[9] is not None:
                item['representativeProduct'] = {
                    'id': row[9],
                    'size': row[10],
                    'basePrice': row[11],
                    'discountRate': row[12],
                    'stock': row[13]
                }
            
            # Manufacturer 정보
            if row[14] is not None:
                item['manufacturer'] = {
                    'id': row[14],
                    'mName': row[15],
                    'mDescription': row[16]
                }
            
            result.append(item)
        
        return {'results': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.get("/{product_base_id}")
async def get_product_base(product_base_id: int):
    """ID로 ProductBase 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
        FROM ProductBase WHERE id = %s
        """
        curs.execute(sql, (product_base_id,))
        row = curs.fetchone()
        
        if row is None:
            return {'result': 'Error', 'message': 'ProductBase not found'}
        
        result = {
            'id': row[0],
            'pName': row[1],
            'pDescription': row[2],
            'pColor': row[3],
            'pGender': row[4],
            'pStatus': row[5],
            'pCategory': row[6],
            'pModelNumber': row[7]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()


@router.post("")
async def create_product_base(product_base: ProductBase):
    """ProductBase 생성"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        INSERT INTO ProductBase 
        (pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (
            product_base.pName,
            product_base.pDescription,
            product_base.pColor,
            product_base.pGender,
            product_base.pStatus,
            product_base.pCategory,
            product_base.pModelNumber
        ))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.put("/{product_base_id}")
async def update_product_base(product_base_id: int, product_base: ProductBase):
    """ProductBase 수정"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        UPDATE ProductBase
        SET pName=%s, pDescription=%s, pColor=%s, pGender=%s, pStatus=%s, pCategory=%s, pModelNumber=%s
        WHERE id=%s
        """
        curs.execute(sql, (
            product_base.pName,
            product_base.pDescription,
            product_base.pColor,
            product_base.pGender,
            product_base.pStatus,
            product_base.pCategory,
            product_base.pModelNumber,
            product_base_id
        ))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


@router.delete("/{product_base_id}")
async def delete_product_base(product_base_id: int):
    """ProductBase 삭제"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = "DELETE FROM ProductBase WHERE id=%s"
        curs.execute(sql, (product_base_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "message": str(e)}
    finally:
        conn.close()


# ============================================
# 복합 쿼리 - /{id}/* 엔드포인트
# ============================================

@router.get("/{product_base_id}/with_images")
async def get_product_base_with_images(product_base_id: int):
    """ProductBase + 이미지 목록 조인 조회"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # ProductBase 정보 조회
        sql_base = """
        SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
        FROM ProductBase WHERE id = %s
        """
        curs.execute(sql_base, (product_base_id,))
        base_row = curs.fetchone()
        
        if base_row is None:
            return {'result': 'Error', 'message': 'ProductBase not found'}
        
        # 이미지 목록 조회
        sql_images = "SELECT imagePath FROM ProductImage WHERE pbid = %s ORDER BY id ASC"
        curs.execute(sql_images, (product_base_id,))
        image_rows = curs.fetchall()
        
        result = {
            'id': base_row[0],
            'pName': base_row[1],
            'pDescription': base_row[2],
            'pColor': base_row[3],
            'pGender': base_row[4],
            'pStatus': base_row[5],
            'pCategory': base_row[6],
            'pModelNumber': base_row[7],
            'images': [row[0] for row in image_rows]
        }
        
        return {'result': result}
    except Exception as e:
        return {'result': 'Error', 'message': str(e)}
    finally:
        conn.close()
