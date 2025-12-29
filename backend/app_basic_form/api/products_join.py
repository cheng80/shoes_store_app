"""
Product 복합 쿼리 API (JOIN)
- Product 중심의 JOIN 쿼리들
- Product + ProductBase + Manufacturer
"""

from fastapi import APIRouter
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# Product + ProductBase
# ============================================
@router.get("/{product_id}/with_base")
async def get_product_with_base(product_id: int):
    """
    특정 Product + ProductBase 정보
    JOIN: Product + ProductBase
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            p.id,
            p.pbid,
            p.mfid,
            p.size,
            p.basePrice,
            p.pQuantity,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pStatus,
            pb.pCategory,
            pb.pModelNumber
        FROM Product p
        JOIN ProductBase pb ON p.pbid = pb.id
        WHERE p.id = %s
        """
        curs.execute(sql, (product_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Product not found"}
        
        result = {
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5],
            'productBase': {
                'pName': row[6],
                'pDescription': row[7],
                'pColor': row[8],
                'pGender': row[9],
                'pStatus': row[10],
                'pCategory': row[11],
                'pModelNumber': row[12]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Product + ProductBase + Manufacturer (3테이블)
# ============================================
@router.get("/{product_id}/with_base_and_manufacturer")
async def get_product_with_base_and_manufacturer(product_id: int):
    """
    특정 Product + ProductBase + Manufacturer 정보
    JOIN: Product + ProductBase + Manufacturer (3테이블)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            p.id,
            p.pbid,
            p.mfid,
            p.size,
            p.basePrice,
            p.pQuantity,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pStatus,
            pb.pCategory,
            pb.pModelNumber,
            m.id as manufacturer_id,
            m.mName
        FROM Product p
        JOIN ProductBase pb ON p.pbid = pb.id
        JOIN Manufacturer m ON p.mfid = m.id
        WHERE p.id = %s
        """
        curs.execute(sql, (product_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Product not found"}
        
        result = {
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5],
            'productBase': {
                'pName': row[6],
                'pDescription': row[7],
                'pColor': row[8],
                'pGender': row[9],
                'pStatus': row[10],
                'pCategory': row[11],
                'pModelNumber': row[12]
            },
            'manufacturer': {
                'id': row[13],
                'mName': row[14]
            }
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase별 Product 목록 + ProductBase 정보
# ============================================
@router.get("/by_pbid/{pbid}/with_base")
async def get_products_by_pbid_with_base(pbid: int):
    """
    특정 ProductBase의 모든 Product + ProductBase 정보
    JOIN: Product + ProductBase
    용도: 상품 상세 화면에서 사이즈별 옵션 표시
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            p.id,
            p.pbid,
            p.mfid,
            p.size,
            p.basePrice,
            p.pQuantity,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pCategory
        FROM Product p
        JOIN ProductBase pb ON p.pbid = pb.id
        WHERE p.pbid = %s
        ORDER BY p.size
        """
        curs.execute(sql, (pbid,))
        rows = curs.fetchall()
        
        if not rows:
            return {"results": [], "message": "No products found for this ProductBase"}
        
        # ProductBase 정보 (첫 번째 행에서 추출)
        first_row = rows[0]
        productBase = {
            'id': first_row[1],
            'pName': first_row[6],
            'pDescription': first_row[7],
            'pColor': first_row[8],
            'pGender': first_row[9],
            'pCategory': first_row[10]
        }
        
        # Product 목록
        products = [{
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5]
        } for row in rows]
        
        return {
            "productBase": productBase,
            "products": products
        }
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# Product 전체 상세 (이미지 포함)
# ============================================
@router.get("/{product_id}/full_detail")
async def get_product_full_detail(product_id: int):
    """
    특정 Product의 전체 상세 정보
    JOIN: Product + ProductBase + Manufacturer + ProductImage
    용도: 상품 상세 화면
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # Product + ProductBase + Manufacturer 조회
        sql = """
        SELECT 
            p.id,
            p.pbid,
            p.mfid,
            p.size,
            p.basePrice,
            p.pQuantity,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pStatus,
            pb.pCategory,
            pb.pModelNumber,
            m.id as manufacturer_id,
            m.mName
        FROM Product p
        JOIN ProductBase pb ON p.pbid = pb.id
        JOIN Manufacturer m ON p.mfid = m.id
        WHERE p.id = %s
        """
        curs.execute(sql, (product_id,))
        row = curs.fetchone()
        
        if row is None:
            return {"result": "Error", "message": "Product not found"}
        
        pbid = row[1]
        
        # 이미지 목록 조회
        sql_images = """
        SELECT imagePath 
        FROM ProductImage 
        WHERE pbid = %s 
        ORDER BY id
        """
        curs.execute(sql_images, (pbid,))
        image_rows = curs.fetchall()
        
        result = {
            'id': row[0],
            'pbid': row[1],
            'mfid': row[2],
            'size': row[3],
            'basePrice': row[4],
            'pQuantity': row[5],
            'productBase': {
                'pName': row[6],
                'pDescription': row[7],
                'pColor': row[8],
                'pGender': row[9],
                'pStatus': row[10],
                'pCategory': row[11],
                'pModelNumber': row[12]
            },
            'manufacturer': {
                'id': row[13],
                'mName': row[14]
            },
            'images': [img[0] for img in image_rows]
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.products_join (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="Product JOIN API Test")
    test_app.include_router(router, prefix="/api/products")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

