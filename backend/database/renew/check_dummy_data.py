"""
데이터베이스 더미 데이터 확인 스크립트
실행: python check_dummy_data.py
"""

import sys
import os

# 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app_new_form.database.connection import connect_db

def check_dummy_data():
    """데이터베이스에 더미 데이터가 있는지 확인"""
    conn = connect_db()
    curs = conn.cursor()
    
    try:
        print("🔍 데이터베이스 더미 데이터 확인 중...\n")
        
        tables = [
            ('branch', '지점'),
            ('maker', '제조사'),
            ('kind_category', '종류 카테고리'),
            ('color_category', '색상 카테고리'),
            ('size_category', '사이즈 카테고리'),
            ('gender_category', '성별 카테고리'),
            ('user', '고객'),
            ('staff', '직원'),
            ('product', '제품'),
            ('purchase_item', '구매 내역'),
            ('pickup', '수령'),
            ('refund', '반품'),
            ('receive', '입고'),
            ('request', '발주'),
        ]
        
        total_count = 0
        for table_name, table_desc in tables:
            curs.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = curs.fetchone()[0]
            total_count += count
            status = "✅" if count > 0 else "❌"
            print(f"{status} {table_desc:20s} ({table_name:20s}): {count:3d}개")
        
        print(f"\n📊 총 데이터 개수: {total_count}개")
        
        if total_count == 0:
            print("\n⚠️  데이터베이스에 더미 데이터가 없습니다.")
        else:
            print("\n✅ 데이터베이스에 더미 데이터가 있습니다.")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    check_dummy_data()

