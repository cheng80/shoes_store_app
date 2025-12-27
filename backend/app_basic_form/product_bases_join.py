"""
ProductBase 복합 쿼리 API
- ProductBase 중심의 JOIN 쿼리들
- ProductBase + ProductImage + Product + Manufacturer

개별 실행: python product_bases_join.py
"""

from fastapi import FastAPI
from database.connection import connect_db

app = FastAPI(title="ProductBase JOIN API")
ipAddress = "127.0.0.1"
port = 8000


# ============================================
# ProductBase + 첫번째 이미지
# ============================================
@app.get("/product_bases/with_first_image")
async def get_product_bases_with_first_image():
    """
    ProductBase 목록 + 첫번째 이미지
    JOIN: ProductBase + ProductImage (서브쿼리)
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pb.id,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pStatus,
            pb.pCategory,
            pb.pModelNumber,
            (SELECT imagePath FROM ProductImage 
             WHERE pbid = pb.id 
             LIMIT 1) as firstImage
        FROM ProductBase pb
        ORDER BY pb.id
        """
        curs.execute(sql)
        rows = curs.fetchall()
        
        result = [{
            'id': row[0],
            'pName': row[1],
            'pDescription': row[2],
            'pColor': row[3],
            'pGender': row[4],
            'pStatus': row[5],
            'pCategory': row[6],
            'pModelNumber': row[7],
            'firstImage': row[8]
        } for row in rows]
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase + 전체 이미지 목록
# ============================================
@app.get("/product_bases/{pbid}/with_images")
async def get_product_base_with_images(pbid: int):
    """
    특정 ProductBase + 전체 이미지 목록
    JOIN: ProductBase + ProductImage
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # ProductBase 정보 조회
        sql_base = """
        SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
        FROM ProductBase 
        WHERE id = %s
        """
        curs.execute(sql_base, (pbid,))
        base_row = curs.fetchone()
        
        if base_row is None:
            return {"result": "Error", "message": "ProductBase not found"}
        
        # 이미지 목록 조회
        sql_images = """
        SELECT id, imagePath 
        FROM ProductImage 
        WHERE pbid = %s 
        ORDER BY id
        """
        curs.execute(sql_images, (pbid,))
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
            'images': [{'id': row[0], 'imagePath': row[1]} for row in image_rows]
        }
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase + Product 목록
# ============================================
@app.get("/product_bases/{pbid}/with_products")
async def get_product_base_with_products(pbid: int):
    """
    특정 ProductBase + 해당 Product 목록 (사이즈별)
    JOIN: ProductBase + Product
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pb.id as pb_id,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pCategory,
            p.id as product_id,
            p.size,
            p.basePrice,
            p.pQuantity,
            p.mfid
        FROM ProductBase pb
        LEFT JOIN Product p ON p.pbid = pb.id
        WHERE pb.id = %s
        ORDER BY p.size
        """
        curs.execute(sql, (pbid,))
        rows = curs.fetchall()
        
        if not rows:
            return {"result": "Error", "message": "ProductBase not found"}
        
        # 첫 번째 행에서 ProductBase 정보 추출
        first_row = rows[0]
        result = {
            'id': first_row[0],
            'pName': first_row[1],
            'pDescription': first_row[2],
            'pColor': first_row[3],
            'pGender': first_row[4],
            'pCategory': first_row[5],
            'products': []
        }
        
        # Product 목록 추가
        for row in rows:
            if row[6] is not None:  # product_id가 있으면
                result['products'].append({
                    'id': row[6],
                    'size': row[7],
                    'basePrice': row[8],
                    'pQuantity': row[9],
                    'mfid': row[10]
                })
        
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase 전체 상세 (4테이블 JOIN)
# ============================================
@app.get("/product_bases/full_detail")
async def get_product_bases_full_detail():
    """
    ProductBase 전체 상세 목록 (검색 화면용)
    JOIN: ProductBase + ProductImage(첫번째) + Product(대표) + Manufacturer
    
    🚀 최적화 API: Flutter에서 여러 번 호출하던 것을 1번으로!
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        sql = """
        SELECT 
            pb.id as pb_id,
            pb.pName,
            pb.pDescription,
            pb.pColor,
            pb.pGender,
            pb.pStatus,
            pb.pCategory,
            pb.pModelNumber,
            (SELECT imagePath FROM ProductImage 
             WHERE pbid = pb.id 
             LIMIT 1) as firstImage,
            p.id as product_id,
            p.size,
            p.basePrice,
            p.pQuantity,
            m.id as manufacturer_id,
            m.mName
        FROM ProductBase pb
        LEFT JOIN Product p ON p.pbid = pb.id AND p.id = (
            SELECT MIN(id) FROM Product WHERE pbid = pb.id
        )
        LEFT JOIN Manufacturer m ON p.mfid = m.id
        ORDER BY pb.id
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
                    'pQuantity': row[12]
                }
            
            # Manufacturer 정보
            if row[13] is not None:
                item['manufacturer'] = {
                    'id': row[13],
                    'mName': row[14]
                }
            
            result.append(item)
        
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# ============================================
if __name__ == "__main__":
    import uvicorn
    print(f"🚀 ProductBase JOIN API 서버 시작")
    print(f"   서버 주소: http://{ipAddress}:{port}")
    print(f"   Swagger UI: http://{ipAddress}:{port}/docs")
    print(f"")
    print(f"   엔드포인트:")
    print(f"   - GET /product_bases/with_first_image")
    print(f"   - GET /product_bases/{{pbid}}/with_images")
    print(f"   - GET /product_bases/{{pbid}}/with_products")
    print(f"   - GET /product_bases/full_detail")
    uvicorn.run(app, host=ipAddress, port=port)

