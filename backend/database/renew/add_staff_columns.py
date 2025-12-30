"""
staff 테이블에 s_id와 s_quit_date 컬럼 추가 스크립트
실행: python add_staff_columns.py
"""

import pymysql
import sys
import os

# 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app_new_form.database.connection import connect_db

def add_staff_columns():
    """staff 테이블에 s_id와 s_quit_date 컬럼 추가"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        print("🔄 staff 테이블 컬럼 추가 시작...")
        
        # 1. s_id 컬럼이 이미 있는지 확인
        curs.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'staff' 
            AND COLUMN_NAME = 's_id'
        """)
        has_s_id = curs.fetchone()[0] > 0
        
        # 2. s_quit_date 컬럼이 이미 있는지 확인
        curs.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'staff' 
            AND COLUMN_NAME = 's_quit_date'
        """)
        has_s_quit_date = curs.fetchone()[0] > 0
        
        # 3. s_id 컬럼 추가
        if not has_s_id:
            print("   📝 s_id 컬럼 추가 중...")
            curs.execute("""
                ALTER TABLE staff 
                ADD COLUMN s_id VARCHAR(50) NOT NULL COMMENT '직원 로그인 ID' AFTER s_seq
            """)
            print("   ✅ s_id 컬럼 추가 완료")
            
            # 기존 데이터에 임시 s_id 값 설정
            print("   📝 기존 데이터에 s_id 값 설정 중...")
            curs.execute("""
                UPDATE staff 
                SET s_id = CONCAT('staff', LPAD(s_seq, 3, '0')) 
                WHERE s_id IS NULL OR s_id = ''
            """)
            print("   ✅ s_id 값 설정 완료")
            
            # UNIQUE 인덱스 추가
            print("   📝 s_id UNIQUE 인덱스 추가 중...")
            curs.execute("""
                ALTER TABLE staff 
                ADD UNIQUE INDEX idx_staff_id (s_id)
            """)
            print("   ✅ s_id 인덱스 추가 완료")
        else:
            print("   ℹ️  s_id 컬럼이 이미 존재합니다.")
        
        # 4. s_quit_date 컬럼 추가
        if not has_s_quit_date:
            print("   📝 s_quit_date 컬럼 추가 중...")
            curs.execute("""
                ALTER TABLE staff 
                ADD COLUMN s_quit_date DATETIME NULL COMMENT '직원 탈퇴 일자' AFTER created_at
            """)
            print("   ✅ s_quit_date 컬럼 추가 완료")
            
            # 인덱스 추가
            print("   📝 s_quit_date 인덱스 추가 중...")
            curs.execute("""
                ALTER TABLE staff 
                ADD INDEX idx_staff_quit_date (s_quit_date)
            """)
            print("   ✅ s_quit_date 인덱스 추가 완료")
        else:
            print("   ℹ️  s_quit_date 컬럼이 이미 존재합니다.")
        
        conn.commit()
        print("\n✅ staff 테이블 컬럼 추가 완료!")
        
        # 확인: 컬럼 목록 조회
        curs.execute("""
            SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_COMMENT
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'staff'
            ORDER BY ORDINAL_POSITION
        """)
        columns = curs.fetchall()
        print("\n📋 staff 테이블 컬럼 목록:")
        for col in columns:
            print(f"   - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'}) - {col[3]}")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ 오류 발생: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    add_staff_columns()

