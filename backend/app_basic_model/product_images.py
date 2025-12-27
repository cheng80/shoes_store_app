"""
ProductImage API - 제품 이미지 CRUD (Model 방식)
개별 실행: python product_images.py

Note: 이미지 파일이 아닌 이미지 경로(URL 문자열)를 저장하므로 JSON Body 방식 사용
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from database.connection import connect_db

app = FastAPI()
ipAddress = "127.0.0.1"


# ============================================
# 모델 정의
# ============================================
class ProductImageCreate(BaseModel):
    pbid: int
    imagePath: str


class ProductImageUpdate(BaseModel):
    id: int
    pbid: int
    imagePath: str


# ============================================
# 전체 제품 이미지 조회
# ============================================
@app.get("/select_product_images")
async def select_product_images():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pbid, imagePath 
        FROM ProductImage 
        ORDER BY id
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'pbid': row[1],
        'imagePath': row[2]
    } for row in rows]
    return {"results": result}


# ============================================
# ProductBase ID로 이미지 조회
# ============================================
@app.get("/select_product_images_by_pbid/{pbid}")
async def select_product_images_by_pbid(pbid: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pbid, imagePath 
        FROM ProductImage 
        WHERE pbid = %s
        ORDER BY id
    """, (pbid,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        'id': row[0],
        'pbid': row[1],
        'imagePath': row[2]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 제품 이미지 조회
# ============================================
@app.get("/select_product_image/{image_id}")
async def select_product_image(image_id: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT id, pbid, imagePath 
        FROM ProductImage 
        WHERE id = %s
    """, (image_id,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "ProductImage not found"}
    result = {
        'id': row[0],
        'pbid': row[1],
        'imagePath': row[2]
    }
    return {"result": result}


# ============================================
# 제품 이미지 추가 (JSON Body)
# ============================================
@app.post("/insert_product_image")
async def insert_product_image(image: ProductImageCreate):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "INSERT INTO ProductImage (pbid, imagePath) VALUES (%s, %s)"
        curs.execute(sql, (image.pbid, image.imagePath))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "id": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제품 이미지 수정 (JSON Body)
# ============================================
@app.post("/update_product_image")
async def update_product_image(image: ProductImageUpdate):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE ProductImage SET pbid=%s, imagePath=%s WHERE id=%s"
        curs.execute(sql, (image.pbid, image.imagePath, image.id))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 제품 이미지 삭제
# ============================================
@app.delete("/delete_product_image/{image_id}")
async def delete_product_image(image_id: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM ProductImage WHERE id=%s"
        curs.execute(sql, (image_id,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=ipAddress, port=8000)
