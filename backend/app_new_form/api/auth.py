"""
소셜 로그인 및 회원가입 완료 API
- 소셜 로그인 후 사용자 생성/조회
- 회원가입 완료 처리
- 회원가입 상태 확인
"""

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from app_new_form.database.connection import connect_db

router = APIRouter()


# ============================================
# 모델 정의
# ============================================
class SocialLoginRequest(BaseModel):
    provider: str  # 'google', 'kakao'
    provider_subject: str  # 구글 sub, 카카오 id
    email: Optional[str] = None
    name: Optional[str] = None
    provider_issuer: Optional[str] = None


class CompleteRegistrationRequest(BaseModel):
    u_name: Optional[str] = None
    u_phone: str  # 필수
    u_address: Optional[str] = None


# ============================================
# 소셜 로그인 (1단계: 사용자 생성/조회)
# ============================================
@router.post("/auth/social/login")
async def social_login(
    provider: str = Form(...),
    provider_subject: str = Form(...),
    email: Optional[str] = Form(None),
    name: Optional[str] = Form(None),
    provider_issuer: Optional[str] = Form(None)
):
    """
    소셜 로그인 후 사용자 생성 또는 조회
    - 기존 사용자면 조회하여 반환
    - 신규 사용자면 기본 정보만 저장하고 미완료 상태로 반환
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 1. user_auth_identities에서 기존 사용자 확인
        curs.execute("""
            SELECT user_id 
            FROM user_auth_identities 
            WHERE provider = %s AND provider_subject = %s
        """, (provider, provider_subject))
        existing_auth = curs.fetchone()
        
        if existing_auth:
            # 기존 사용자: user 정보 조회
            user_id = existing_auth[0]
            curs.execute("""
                SELECT u_seq, u_name, u_email, u_phone, u_address, registration_completed
                FROM user 
                WHERE u_seq = %s
            """, (user_id,))
            user_row = curs.fetchone()
            
            if user_row:
                return {
                    "result": "OK",
                    "user_seq": user_row[0],
                    "u_name": user_row[1],
                    "u_email": user_row[2],
                    "u_phone": user_row[3],
                    "u_address": user_row[4],
                    "registration_completed": bool(user_row[5]),
                    "message": "기존 사용자 로그인 성공"
                }
        
        # 2. 신규 사용자: user 테이블에 기본 정보만 저장
        curs.execute("""
            INSERT INTO user (u_email, u_name, u_phone, registration_completed)
            VALUES (%s, %s, NULL, FALSE)
        """, (email, name))
        user_seq = curs.lastrowid
        
        # 3. user_auth_identities에 소셜 로그인 정보 저장
        curs.execute("""
            INSERT INTO user_auth_identities 
            (user_id, provider, provider_subject, provider_issuer, email_at_provider)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_seq, provider, provider_subject, provider_issuer, email))
        
        conn.commit()
        
        return {
            "result": "OK",
            "user_seq": user_seq,
            "u_name": name,
            "u_email": email,
            "u_phone": None,
            "u_address": None,
            "registration_completed": False,
            "message": "소셜 로그인 성공. 추가 정보 입력이 필요합니다."
        }
        
    except Exception as e:
        conn.rollback()
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 회원가입 완료 (2단계: 추가 정보 입력)
# ============================================
@router.post("/users/{user_seq}/complete_registration")
async def complete_registration(
    user_seq: int,
    u_name: Optional[str] = Form(None),
    u_phone: str = Form(...),
    u_address: Optional[str] = Form(None)
):
    """
    소셜 로그인 사용자의 회원가입 완료 처리
    - 필수 필드: u_phone
    - 선택 필드: u_name (수정), u_address
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        # 1. 사용자 존재 확인
        curs.execute("SELECT u_seq FROM user WHERE u_seq = %s", (user_seq,))
        if not curs.fetchone():
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        # 2. 필수 필드 검증
        if not u_phone or u_phone.strip() == "":
            raise HTTPException(status_code=400, detail="전화번호는 필수 입력 항목입니다")
        
        # 3. 전화번호 중복 확인
        curs.execute("""
            SELECT u_seq FROM user 
            WHERE u_phone = %s AND u_seq != %s
        """, (u_phone, user_seq))
        if curs.fetchone():
            raise HTTPException(status_code=400, detail="이미 사용 중인 전화번호입니다")
        
        # 4. 사용자 정보 업데이트
        if u_name:
            # 이름 수정
            curs.execute("""
                UPDATE user 
                SET u_name = %s, u_phone = %s, u_address = %s, registration_completed = TRUE
                WHERE u_seq = %s
            """, (u_name, u_phone, u_address, user_seq))
        else:
            # 이름 수정 없음
            curs.execute("""
                UPDATE user 
                SET u_phone = %s, u_address = %s, registration_completed = TRUE
                WHERE u_seq = %s
            """, (u_phone, u_address, user_seq))
        
        conn.commit()
        
        return {
            "result": "OK",
            "message": "회원가입이 완료되었습니다"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 회원가입 완료 상태 확인
# ============================================
@router.get("/users/{user_seq}/registration_status")
async def get_registration_status(user_seq: int):
    """
    사용자의 회원가입 완료 상태 확인
    - 미완료인 경우 누락된 필드 목록 반환
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        curs.execute("""
            SELECT u_seq, u_name, u_email, u_phone, u_address, registration_completed
            FROM user 
            WHERE u_seq = %s
        """, (user_seq,))
        row = curs.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        missing_fields = []
        if not row[3] or row[3].strip() == "":  # u_phone
            missing_fields.append("u_phone")
        # u_address는 선택 사항이므로 제외하거나 비즈니스 요구사항에 따라 추가
        
        return {
            "result": {
                "user_seq": row[0],
                "registration_completed": bool(row[5]),
                "missing_fields": missing_fields,
                "has_phone": bool(row[3] and row[3].strip() != ""),
                "has_address": bool(row[4] and row[4].strip() != "")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        return {"result": "Error", "errorMsg": str(e)}
    finally:
        conn.close()


# ============================================
# 회원가입 완료 여부 확인 데코레이터 (미들웨어용)
# ============================================
def check_registration_completed(user_seq: int):
    """
    회원가입 완료 여부 확인
    미완료인 경우 HTTPException 발생
    """
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        curs.execute("""
            SELECT registration_completed 
            FROM user 
            WHERE u_seq = %s
        """, (user_seq,))
        row = curs.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        if not row[0]:
            raise HTTPException(
                status_code=403,
                detail="회원가입을 완료해주세요. 추가 정보 입력이 필요합니다."
            )
        
    finally:
        conn.close()

