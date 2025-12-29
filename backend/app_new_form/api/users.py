"""
User API - 고객 계정 CRUD (Form 방식)
개별 실행: python users.py

Note: INSERT는 이미지 포함 필수, UPDATE는 이미지 제외/포함 두 가지 방식 제공
"""

from fastapi import APIRouter, Form, UploadFile, File, Response
from pydantic import BaseModel
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class User(BaseModel):
    u_seq: Optional[int] = None
    u_id: str
    u_password: str
    u_name: str
    u_phone: str


# ============================================
# 전체 고객 조회 (이미지 제외)
# ============================================
@router.get("")
async def select_users():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT u_seq, u_id, u_password, u_name, u_phone 
        FROM user 
        ORDER BY u_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        'u_seq': row[0],
        'u_id': row[1],
        'u_password': row[2],
        'u_name': row[3],
        'u_phone': row[4]
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 고객 조회 (이미지 제외)
# ============================================
@router.get("/{user_seq}")
async def select_user(user_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT u_seq, u_id, u_password, u_name, u_phone 
        FROM user 
        WHERE u_seq = %s
    """, (user_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "User not found"}
    result = {
        'u_seq': row[0],
        'u_id': row[1],
        'u_password': row[2],
        'u_name': row[3],
        'u_phone': row[4]
    }
    return {"result": result}


# ============================================
# 고객 추가 (이미지 포함 필수 - Form + UploadFile)
# ============================================
@router.post("")
async def insert_user(
    u_id: str = Form(...),
    u_password: str = Form(...),
    u_name: str = Form(...),
    u_phone: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO user (u_id, u_password, u_name, u_phone, u_image) 
            VALUES (%s, %s, %s, %s, %s)
        """
        curs.execute(sql, (u_id, u_password, u_name, u_phone, image_data))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "u_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 수정 (이미지 제외 - Form)
# ============================================
@router.post("/{user_seq}")
async def update_user(
    user_seq: int,
    u_id: str = Form(...),
    u_password: str = Form(...),
    u_name: str = Form(...),
    u_phone: str = Form(...),
):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE user 
            SET u_id=%s, u_password=%s, u_name=%s, u_phone=%s 
            WHERE u_seq=%s
        """
        curs.execute(sql, (u_id, u_password, u_name, u_phone, user_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 수정 (이미지 포함 - Form + UploadFile)
# ============================================
@router.post("/{user_seq}/with_image")
async def update_user_with_image(
    user_seq: int,
    u_id: str = Form(...),
    u_password: str = Form(...),
    u_name: str = Form(...),
    u_phone: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE user 
            SET u_id=%s, u_password=%s, u_name=%s, u_phone=%s, u_image=%s 
            WHERE u_seq=%s
        """
        curs.execute(sql, (u_id, u_password, u_name, u_phone, image_data, user_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 프로필 이미지 조회 (Response - 바이너리 직접 반환)
# ============================================
@router.get("/{user_seq}/profile_image")
async def view_user_profile_image(user_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        curs.execute("SELECT u_image FROM user WHERE u_seq = %s", (user_seq,))
        row = curs.fetchone()
        conn.close()
        
        if row is None:
            return {"result": "Error", "message": "User not found"}
        
        if row[0] is None:
            return {"result": "Error", "message": "No profile image"}
        
        # Response 객체로 바이너리 직접 반환
        return Response(
            content=row[0],
            media_type="image/jpeg",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 프로필 이미지 삭제
# ============================================
@router.delete("/{user_seq}/profile_image")
async def delete_user_profile_image(user_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE user SET u_image=NULL WHERE u_seq=%s"
        curs.execute(sql, (user_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 고객 삭제
# ============================================
@router.delete("/{user_seq}")
async def delete_user(user_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM user WHERE u_seq=%s"
        curs.execute(sql, (user_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

