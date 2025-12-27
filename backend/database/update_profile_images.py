"""
기존 Customer/Employee 데이터에 더미 프로필 이미지 추가
"""

import sys
sys.path.insert(0, '/Users/cheng80/Git_Work/shoes_store_app/backend')

from app_basic.database.connection import connect_db


# 1x1 픽셀 투명 PNG 이미지 (테스트용 플레이스홀더)
PLACEHOLDER_PNG = bytes.fromhex(
    '89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C489'
    '0000000A49444154789C6300010000050001E2D9A4B50000000049454E44AE426082'
)


def update_profile_images():
    """기존 데이터에 플레이스홀더 이미지 추가"""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Customer - 처음 3명에게 이미지 추가 (조조, 손책, 유비)
        print("Customer 프로필 이미지 업데이트 중...")
        cursor.execute("""
            UPDATE Customer 
            SET cProfileImage = %s 
            WHERE id IN (1, 2, 3)
        """, (PLACEHOLDER_PNG,))
        print(f"  ✅ {cursor.rowcount}명 업데이트됨")
        
        # Employee - 처음 2명에게 이미지 추가 (사마의, 주유)
        print("Employee 프로필 이미지 업데이트 중...")
        cursor.execute("""
            UPDATE Employee 
            SET eProfileImage = %s 
            WHERE id IN (1, 2)
        """, (PLACEHOLDER_PNG,))
        print(f"  ✅ {cursor.rowcount}명 업데이트됨")
        
        conn.commit()
        print("\n🎉 프로필 이미지 업데이트 완료!")
        
        # 결과 확인
        print("\n" + "="*60)
        print("Customer 프로필 이미지 상태:")
        print("="*60)
        cursor.execute("""
            SELECT id, cName, 
                   CASE WHEN cProfileImage IS NULL THEN '❌ 없음' 
                        ELSE CONCAT('✅ ', LENGTH(cProfileImage), ' bytes') 
                   END as profileStatus
            FROM Customer
        """)
        for row in cursor.fetchall():
            print(f"  ID {row[0]:2} | {row[1]:10} | {row[2]}")
        
        print("\n" + "="*60)
        print("Employee 프로필 이미지 상태:")
        print("="*60)
        cursor.execute("""
            SELECT id, eName, 
                   CASE WHEN eProfileImage IS NULL THEN '❌ 없음' 
                        ELSE CONCAT('✅ ', LENGTH(eProfileImage), ' bytes') 
                   END as profileStatus
            FROM Employee
        """)
        for row in cursor.fetchall():
            print(f"  ID {row[0]:2} | {row[1]:10} | {row[2]}")
            
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    update_profile_images()

