"""
ProductBase API - 제품 기본정보 CRUD (Form 방식)
"""

from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import Optional
from app_basic_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class ProductBase(BaseModel):
    id: Optional[int] = None
    pName: str
    pDescription: str
    pColor: str
    pGender: str
    pStatus: str
    pCategory: str
    pModelNumber: str


# ============================================
# 전체 ProductBase 조회
# ============================================
@router.get("")
async def select_product_bases():
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
            FROM ProductBase 
            ORDER BY id
        """)
        rows = curs.fetchall()
        result = [{
            'id': row[0],
            'pName': row[1],
            'pDescription': row[2],
            'pColor': row[3],
            'pGender': row[4],
            'pStatus': row[5],
            'pCategory': row[6],
            'pModelNumber': row[7]
        } for row in rows]
        return {"results": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ID로 ProductBase 조회
# ============================================
@router.get("/{product_base_id}")
async def select_product_base(product_base_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT id, pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber 
            FROM ProductBase 
            WHERE id = %s
        """, (product_base_id,))
        row = curs.fetchone()
        if row is None:
            return {"result": "Error", "message": "ProductBase not found"}
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
        return {"result": result}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase 추가
# ============================================
@router.post("")
async def insert_product_base(
    pName: str = Form(...),
    pDescription: str = Form(...),
    pColor: str = Form(...),
    pGender: str = Form(...),
    pStatus: str = Form(...),
    pCategory: str = Form(...),
    pModelNumber: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            INSERT INTO ProductBase 
            (pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber))
        conn.commit()
        inserted_id = curs.lastrowid
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase 수정
# ============================================
@router.post("/{product_base_id}")
async def update_product_base(
    product_base_id: int,
    pName: str = Form(...),
    pDescription: str = Form(...),
    pColor: str = Form(...),
    pGender: str = Form(...),
    pStatus: str = Form(...),
    pCategory: str = Form(...),
    pModelNumber: str = Form(...),
):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = """
            UPDATE ProductBase 
            SET pName=%s, pDescription=%s, pColor=%s, pGender=%s, pStatus=%s, pCategory=%s, pModelNumber=%s 
            WHERE id=%s
        """
        curs.execute(sql, (pName, pDescription, pColor, pGender, pStatus, pCategory, pModelNumber, product_base_id))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# ProductBase 삭제
# ============================================
@router.delete("/{product_base_id}")
async def delete_product_base(product_base_id: int):
    conn = connect_db()
    curs = conn.cursor()
    try:
        sql = "DELETE FROM ProductBase WHERE id=%s"
        curs.execute(sql, (product_base_id,))
        conn.commit()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 개별 실행용 (테스트)
# 실행: python -m app_basic_form.api.product_bases (backend 폴더에서)
# ============================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

if __name__ == "__main__":
    from fastapi import FastAPI
    import uvicorn
    
    test_app = FastAPI(title="ProductBase API Test")
    test_app.include_router(router, prefix="/api/product_bases")
    uvicorn.run(test_app, host=SERVER_HOST, port=SERVER_PORT)

