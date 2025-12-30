"""
더미 데이터 생성 스크립트의 중복 방지 로직 검수
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app_new_form.database.connection import connect_db

def check_duplicate_prevention():
    """중복 방지 로직 검수"""
    conn = connect_db()
    curs = conn.cursor()
    
    print("🔍 중복 방지 로직 검수 시작...\n")
    
    # UNIQUE 제약조건이 있는 테이블과 컬럼 확인
    unique_constraints = {
        'branch': ['br_name'],
        'user': ['u_id', 'u_phone'],
        'staff': ['s_id', 's_phone'],
        'maker': ['m_name'],
        'kind_category': ['kc_name'],
        'color_category': ['cc_name'],
        'size_category': ['sc_name'],
        'gender_category': ['gc_name'],
        'refund_reason_category': ['ref_re_name'],
    }
    
    # product 테이블의 복합 UNIQUE 제약조건
    product_unique = ['cc_seq', 'sc_seq', 'm_seq']
    
    print("📋 UNIQUE 제약조건이 있는 테이블:\n")
    for table, columns in unique_constraints.items():
        print(f"   - {table}: {', '.join(columns)}")
    print(f"   - product: ({', '.join(product_unique)}) 조합\n")
    
    # 각 테이블의 중복 데이터 확인
    print("🔍 중복 데이터 확인:\n")
    duplicates_found = False
    
    for table, columns in unique_constraints.items():
        for column in columns:
            curs.execute(f"""
                SELECT {column}, COUNT(*) as cnt
                FROM {table}
                GROUP BY {column}
                HAVING cnt > 1
            """)
            duplicates = curs.fetchall()
            if duplicates:
                duplicates_found = True
                print(f"   ❌ {table}.{column}: 중복 발견!")
                for dup in duplicates:
                    print(f"      - '{dup[0]}': {dup[1]}개")
            else:
                print(f"   ✅ {table}.{column}: 중복 없음")
    
    # product 테이블의 복합 UNIQUE 확인
    curs.execute(f"""
        SELECT {', '.join(product_unique)}, COUNT(*) as cnt
        FROM product
        GROUP BY {', '.join(product_unique)}
        HAVING cnt > 1
    """)
    product_duplicates = curs.fetchall()
    if product_duplicates:
        duplicates_found = True
        print(f"\n   ❌ product ({', '.join(product_unique)}): 중복 발견!")
        for dup in product_duplicates:
            print(f"      - {dict(zip(product_unique, dup[:-1]))}: {dup[-1]}개")
    else:
        print(f"\n   ✅ product ({', '.join(product_unique)}): 중복 없음")
    
    print("\n" + "="*60)
    if duplicates_found:
        print("⚠️  중복 데이터가 발견되었습니다!")
    else:
        print("✅ 중복 데이터가 없습니다.")
    print("="*60)
    
    conn.close()

if __name__ == "__main__":
    check_duplicate_prevention()

