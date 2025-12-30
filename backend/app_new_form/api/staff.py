"""
Staff API - 직원 계정 CRUD (Form 방식)
개별 실행: python staff.py

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
class Staff(BaseModel):
    s_seq: Optional[int] = None
    s_id: str
    br_seq: int
    s_password: str
    s_name: str
    s_rank: Optional[str] = None
    s_phone: str
    s_superseq: Optional[int] = None
    created_at: Optional[str] = None
    s_quit_date: Optional[str] = None


# ============================================
# 전체 직원 조회 (이미지 제외)
# ============================================
@router.get("")
async def select_staffs():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT s_seq, s_id, br_seq, s_password, s_name, s_rank, s_phone, s_superseq, created_at, s_quit_date 
        FROM staff 
        ORDER BY s_seq
    """)
    rows = curs.fetchall()
    conn.close()
    result = [{
        's_seq': row[0],
        's_id': row[1],
        'br_seq': row[2],
        's_password': row[3],
        's_name': row[4],
        's_rank': row[5],
        's_phone': row[6],
        's_superseq': row[7],
        'created_at': row[8].isoformat() if row[8] else None,
        's_quit_date': row[9].isoformat() if row[9] else None
    } for row in rows]
    return {"results": result}


# ============================================
# ID로 직원 조회 (이미지 제외)
# ============================================
@router.get("/{staff_seq}")
async def select_staff(staff_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT s_seq, s_id, br_seq, s_password, s_name, s_rank, s_phone, s_superseq, created_at, s_quit_date 
        FROM staff 
        WHERE s_seq = %s
    """, (staff_seq,))
    row = curs.fetchone()
    conn.close()
    if row is None:
        return {"result": "Error", "message": "Staff not found"}
    result = {
        's_seq': row[0],
        's_id': row[1],
        'br_seq': row[2],
        's_password': row[3],
        's_name': row[4],
        's_rank': row[5],
        's_phone': row[6],
        's_superseq': row[7],
        'created_at': row[8].isoformat() if row[8] else None,
        's_quit_date': row[9].isoformat() if row[9] else None
    }
    return {"result": result}


# ============================================
# 지점별 직원 조회
# ============================================
@router.get("/by_branch/{branch_seq}")
async def select_staffs_by_branch(branch_seq: int):
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
        SELECT s_seq, s_id, br_seq, s_password, s_name, s_rank, s_phone, s_superseq, created_at, s_quit_date 
        FROM staff 
        WHERE br_seq = %s
        ORDER BY s_seq
    """, (branch_seq,))
    rows = curs.fetchall()
    conn.close()
    result = [{
        's_seq': row[0],
        's_id': row[1],
        'br_seq': row[2],
        's_password': row[3],
        's_name': row[4],
        's_rank': row[5],
        's_phone': row[6],
        's_superseq': row[7],
        'created_at': row[8].isoformat() if row[8] else None,
        's_quit_date': row[9].isoformat() if row[9] else None
    } for row in rows]
    return {"results": result}


# ============================================
# 직원 추가 (이미지 포함 필수 - Form + UploadFile)
# ============================================
@router.post("")
async def insert_staff(
    s_id: str = Form(...),
    br_seq: int = Form(...),
    s_password: str = Form(...),
    s_name: str = Form(...),
    s_phone: str = Form(...),
    s_rank: Optional[str] = Form(None),
    s_superseq: Optional[int] = Form(None),
    file: UploadFile = File(...)
):
    try:
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            INSERT INTO staff (s_id, br_seq, s_password, s_name, s_phone, s_rank, s_superseq, s_image) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        curs.execute(sql, (s_id, br_seq, s_password, s_name, s_phone, s_rank, s_superseq, image_data))
        conn.commit()
        inserted_id = curs.lastrowid
        conn.close()
        return {"result": "OK", "s_seq": inserted_id}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 직원 수정 (이미지 제외 - Form)
# ============================================
@router.post("/{id}")
async def update_staff(
    s_seq: int = Form(...),
    s_id: str = Form(...),
    br_seq: int = Form(...),
    s_password: str = Form(...),
    s_name: str = Form(...),
    s_phone: str = Form(...),
    s_rank: Optional[str] = Form(None),
    s_superseq: Optional[int] = Form(None),
    s_quit_date: Optional[str] = Form(None),
):
    try:
        from datetime import datetime
        s_quit_date_dt = None
        if s_quit_date:
            s_quit_date_dt = datetime.fromisoformat(s_quit_date.replace('Z', '+00:00'))
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE staff 
            SET s_id=%s, br_seq=%s, s_password=%s, s_name=%s, s_phone=%s, s_rank=%s, s_superseq=%s, s_quit_date=%s 
            WHERE s_seq=%s
        """
        curs.execute(sql, (s_id, br_seq, s_password, s_name, s_phone, s_rank, s_superseq, s_quit_date_dt, s_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 직원 수정 (이미지 포함 - Form + UploadFile)
# ============================================
@router.post("/{id}/with_image")
async def update_staff_with_image(
    s_seq: int = Form(...),
    s_id: str = Form(...),
    br_seq: int = Form(...),
    s_password: str = Form(...),
    s_name: str = Form(...),
    s_phone: str = Form(...),
    s_rank: Optional[str] = Form(None),
    s_superseq: Optional[int] = Form(None),
    s_quit_date: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    try:
        from datetime import datetime
        s_quit_date_dt = None
        if s_quit_date:
            s_quit_date_dt = datetime.fromisoformat(s_quit_date.replace('Z', '+00:00'))
        
        # 파일 읽기
        image_data = await file.read()
        
        conn = connect_db()
        curs = conn.cursor()
        sql = """
            UPDATE staff 
            SET s_id=%s, br_seq=%s, s_password=%s, s_name=%s, s_phone=%s, s_rank=%s, s_superseq=%s, s_quit_date=%s, s_image=%s 
            WHERE s_seq=%s
        """
        curs.execute(sql, (s_id, br_seq, s_password, s_name, s_phone, s_rank, s_superseq, s_quit_date_dt, image_data, s_seq))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 프로필 이미지 조회 (Response - 바이너리 직접 반환)
# ============================================
@router.get("/staff_seq/profile_image")
async def view_staff_profile_image(staff_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        curs.execute("SELECT s_image FROM staff WHERE s_seq = %s", (staff_seq,))
        row = curs.fetchone()
        conn.close()
        
        if row is None:
            return {"result": "Error", "message": "Staff not found"}
        
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
@router.delete("/{staff_seq}")
async def delete_staff_profile_image(staff_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "UPDATE staff SET s_image=NULL WHERE s_seq=%s"
        curs.execute(sql, (staff_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}


# ============================================
# 직원 삭제
# ============================================
@router.delete("/{staff_seq}")
async def delete_staff(staff_seq: int):
    try:
        conn = connect_db()
        curs = conn.cursor()
        sql = "DELETE FROM staff WHERE s_seq=%s"
        curs.execute(sql, (staff_seq,))
        conn.commit()
        conn.close()
        return {"result": "OK"}
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}

