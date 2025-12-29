"""
app_new_form API 테스트 스크립트

각 파일을 개별 실행 후 이 스크립트로 테스트합니다.

사용법:
    1. 테스트할 파일 실행: python branch.py
    2. 테스트 실행: python TEST/test_app_new_form.py branch

작성일: 2025-01-XX
"""

import httpx
import sys
import random
from typing import Optional

# ============================================
# 설정
# ============================================
BASE_URL = 'http://127.0.0.1:8000'

test_results = {
    'passed': 0,
    'failed': 0,
    'tests': []
}


# ============================================
# 유틸리티 함수
# ============================================
def print_header(title: str):
    print('\n' + '=' * 60)
    print(f'🧪 {title}')
    print('=' * 60)


def print_test(name: str, success: bool, detail: str = ''):
    icon = '✅' if success else '❌'
    print(f'   {icon} {name}')
    if detail:
        print(f'      {detail}')
    
    test_results['tests'].append({
        'name': name,
        'success': success,
        'detail': detail
    })
    
    if success:
        test_results['passed'] += 1
    else:
        test_results['failed'] += 1


def api_get(endpoint: str) -> dict:
    try:
        response = httpx.get(f'{BASE_URL}{endpoint}', timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}


def api_post_form(endpoint: str, data: dict) -> dict:
    try:
        response = httpx.post(f'{BASE_URL}{endpoint}', data=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}


def api_post_form_with_file(endpoint: str, data: dict, file_path: str = None) -> dict:
    """Form 데이터와 파일 업로드"""
    try:
        files = None
        if file_path:
            # 더미 이미지 파일 생성 (1x1 PNG)
            import io
            dummy_image = io.BytesIO(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\xe2\xd9\xa4\xb5\x00\x00\x00\x00IEND\xaeB`\x82')
            files = {'file': ('test.png', dummy_image, 'image/png')}
        
        response = httpx.post(f'{BASE_URL}{endpoint}', data=data, files=files, timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}


def api_delete(endpoint: str) -> dict:
    try:
        response = httpx.delete(f'{BASE_URL}{endpoint}', timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}


# ============================================
# Branch 테스트
# ============================================
def test_branch():
    print_header('Branch API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_branches')
    success = 'results' in result
    print_test('전체 지점 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 지점 추가
    uid = random.randint(10000, 99999)
    new_branch = {
        'br_name': f'테스트지점{uid}',
        'br_phone': f'02-{uid}-0000',
        'br_address': f'서울시 테스트구 테스트로 {uid}',
        'br_lat': '37.5010',
        'br_lng': '127.0260'
    }
    result = api_post_form('/insert_branch', new_branch)
    branch_seq = result.get('br_seq')
    success = result.get('result') == 'OK' and branch_seq is not None
    print_test('지점 추가', success, f"br_seq: {branch_seq}")
    
    # 3. ID로 조회
    if branch_seq:
        result = api_get(f'/select_branch/{branch_seq}')
        success = 'result' in result
        print_test('ID로 지점 조회', success)
    
    # 4. 지점 수정
    if branch_seq:
        update_data = {
            'br_seq': branch_seq,
            'br_name': f'수정된지점{uid}',
            'br_phone': f'02-{uid}-1111',
            'br_address': f'서울시 수정구 수정로 {uid}',
            'br_lat': '37.5020',
            'br_lng': '127.0270'
        }
        result = api_post_form('/update_branch', update_data)
        success = result.get('result') == 'OK'
        print_test('지점 수정', success)
    
    # 5. 지점 삭제
    if branch_seq:
        result = api_delete(f'/delete_branch/{branch_seq}')
        success = result.get('result') == 'OK'
        print_test('지점 삭제', success)


# ============================================
# Users 테스트
# ============================================
def test_users():
    print_header('Users API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_users')
    success = 'results' in result
    print_test('전체 고객 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 고객 추가 (이미지 포함 필수)
    uid = random.randint(10000, 99999)
    new_user = {
        'u_id': f'user_test{uid}',
        'u_password': 'testpass',
        'u_name': '테스트고객',
        'u_phone': f'010-{uid}-9999'
    }
    result = api_post_form_with_file('/insert_user', new_user, 'dummy.png')
    user_seq = result.get('u_seq')
    success = result.get('result') == 'OK' and user_seq is not None
    print_test('고객 추가 (이미지 포함)', success, f"u_seq: {user_seq}")
    
    # 3. ID로 조회
    if user_seq:
        result = api_get(f'/select_user/{user_seq}')
        success = 'result' in result
        print_test('ID로 고객 조회', success)
    
    # 4. 고객 수정 (이미지 제외)
    if user_seq:
        update_data = {
            'u_seq': user_seq,
            'u_id': f'user_updated{uid}',
            'u_password': 'newpass',
            'u_name': '수정된고객',
            'u_phone': f'010-{uid}-8888'
        }
        result = api_post_form('/update_user', update_data)
        success = result.get('result') == 'OK'
        print_test('고객 수정 (이미지 제외)', success)
    
    # 5. 고객 수정 (이미지 포함)
    if user_seq:
        update_data = {
            'u_seq': user_seq,
            'u_id': f'user_img{uid}',
            'u_password': 'newpass',
            'u_name': '이미지수정고객',
            'u_phone': f'010-{uid}-7777'
        }
        result = api_post_form_with_file('/update_user_with_image', update_data, 'dummy.png')
        success = result.get('result') == 'OK'
        print_test('고객 수정 (이미지 포함)', success)
    
    # 6. 프로필 이미지 조회
    if user_seq:
        try:
            response = httpx.get(f'{BASE_URL}/view_user_profile_image/{user_seq}', timeout=10)
            success = response.status_code == 200 and response.headers.get('content-type', '').startswith('image/')
            print_test('프로필 이미지 조회', success)
        except Exception as e:
            print_test('프로필 이미지 조회', False, str(e))
    
    # 7. 고객 삭제
    if user_seq:
        result = api_delete(f'/delete_user/{user_seq}')
        success = result.get('result') == 'OK'
        print_test('고객 삭제', success)


# ============================================
# Staff 테스트
# ============================================
def test_staff():
    print_header('Staff API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_staffs')
    success = 'results' in result
    print_test('전체 직원 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 지점 조회 (branch 데이터 필요)
    branches_result = api_get('/select_branches')
    if branches_result.get('results'):
        branch_seq = branches_result['results'][0]['br_seq']
        result = api_get(f'/select_staffs_by_branch/{branch_seq}')
        success = 'results' in result
        print_test('지점별 직원 조회', success)
    
    # 3. 직원 추가 (이미지 포함 필수)
    uid = random.randint(10000, 99999)
    if branches_result.get('results'):
        branch_seq = branches_result['results'][0]['br_seq']
        new_staff = {
            'br_seq': branch_seq,
            's_password': 'testpass',
            's_phone': f'010-{uid}-6666',
            's_rank': '사원'
        }
        result = api_post_form_with_file('/insert_staff', new_staff, 'dummy.png')
        staff_seq = result.get('s_seq')
        success = result.get('result') == 'OK' and staff_seq is not None
        print_test('직원 추가 (이미지 포함)', success, f"s_seq: {staff_seq}")
        
        # 4. ID로 조회
        if staff_seq:
            result = api_get(f'/select_staff/{staff_seq}')
            success = 'result' in result
            print_test('ID로 직원 조회', success)
        
        # 5. 직원 삭제
        if staff_seq:
            result = api_delete(f'/delete_staff/{staff_seq}')
            success = result.get('result') == 'OK'
            print_test('직원 삭제', success)


# ============================================
# Maker 테스트
# ============================================
def test_maker():
    print_header('Maker API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_makers')
    success = 'results' in result
    print_test('전체 제조사 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 제조사 추가
    uid = random.randint(10000, 99999)
    new_maker = {
        'm_name': f'테스트제조사{uid}',
        'm_phone': f'02-{uid}-2222',
        'm_address': f'서울시 제조사구 제조사로 {uid}'
    }
    result = api_post_form('/insert_maker', new_maker)
    maker_seq = result.get('m_seq')
    success = result.get('result') == 'OK' and maker_seq is not None
    print_test('제조사 추가', success, f"m_seq: {maker_seq}")
    
    # 3. ID로 조회
    if maker_seq:
        result = api_get(f'/select_maker/{maker_seq}')
        success = 'result' in result
        print_test('ID로 제조사 조회', success)
    
    # 4. 제조사 수정
    if maker_seq:
        update_data = {
            'm_seq': maker_seq,
            'm_name': f'수정된제조사{uid}',
            'm_phone': f'02-{uid}-3333',
            'm_address': f'서울시 수정구 수정로 {uid}'
        }
        result = api_post_form('/update_maker', update_data)
        success = result.get('result') == 'OK'
        print_test('제조사 수정', success)
    
    # 5. 제조사 삭제
    if maker_seq:
        result = api_delete(f'/delete_maker/{maker_seq}')
        success = result.get('result') == 'OK'
        print_test('제조사 삭제', success)


# ============================================
# Category 테스트 (kind, color, size, gender)
# ============================================
def test_kind_category():
    print_header('KindCategory API 테스트')
    
    result = api_get('/select_kind_categories')
    success = 'results' in result
    print_test('전체 종류 카테고리 조회', success, f"조회: {len(result.get('results', []))}건")
    
    uid = random.randint(10000, 99999)
    new_category = {'kc_name': f'테스트종류{uid}'}
    result = api_post_form('/insert_kind_category', new_category)
    kc_seq = result.get('kc_seq')
    success = result.get('result') == 'OK' and kc_seq is not None
    print_test('종류 카테고리 추가', success, f"kc_seq: {kc_seq}")
    
    if kc_seq:
        result = api_get(f'/select_kind_category/{kc_seq}')
        success = 'result' in result
        print_test('ID로 종류 카테고리 조회', success)
        
        result = api_delete(f'/delete_kind_category/{kc_seq}')
        success = result.get('result') == 'OK'
        print_test('종류 카테고리 삭제', success)


def test_color_category():
    print_header('ColorCategory API 테스트')
    
    result = api_get('/select_color_categories')
    success = 'results' in result
    print_test('전체 색상 카테고리 조회', success, f"조회: {len(result.get('results', []))}건")
    
    uid = random.randint(10000, 99999)
    new_category = {'cc_name': f'테스트색상{uid}'}
    result = api_post_form('/insert_color_category', new_category)
    cc_seq = result.get('cc_seq')
    success = result.get('result') == 'OK' and cc_seq is not None
    print_test('색상 카테고리 추가', success, f"cc_seq: {cc_seq}")
    
    if cc_seq:
        result = api_get(f'/select_color_category/{cc_seq}')
        success = 'result' in result
        print_test('ID로 색상 카테고리 조회', success)
        
        result = api_delete(f'/delete_color_category/{cc_seq}')
        success = result.get('result') == 'OK'
        print_test('색상 카테고리 삭제', success)


def test_size_category():
    print_header('SizeCategory API 테스트')
    
    result = api_get('/select_size_categories')
    success = 'results' in result
    print_test('전체 사이즈 카테고리 조회', success, f"조회: {len(result.get('results', []))}건")
    
    uid = random.randint(10000, 99999)
    new_category = {'sc_name': f'{250 + uid % 10}'}
    result = api_post_form('/insert_size_category', new_category)
    sc_seq = result.get('sc_seq')
    success = result.get('result') == 'OK' and sc_seq is not None
    print_test('사이즈 카테고리 추가', success, f"sc_seq: {sc_seq}")
    
    if sc_seq:
        result = api_get(f'/select_size_category/{sc_seq}')
        success = 'result' in result
        print_test('ID로 사이즈 카테고리 조회', success)
        
        result = api_delete(f'/delete_size_category/{sc_seq}')
        success = result.get('result') == 'OK'
        print_test('사이즈 카테고리 삭제', success)


def test_gender_category():
    print_header('GenderCategory API 테스트')
    
    result = api_get('/select_gender_categories')
    success = 'results' in result
    print_test('전체 성별 카테고리 조회', success, f"조회: {len(result.get('results', []))}건")
    
    uid = random.randint(10000, 99999)
    new_category = {'gc_name': '테스트성별'}
    result = api_post_form('/insert_gender_category', new_category)
    gc_seq = result.get('gc_seq')
    success = result.get('result') == 'OK' and gc_seq is not None
    print_test('성별 카테고리 추가', success, f"gc_seq: {gc_seq}")
    
    if gc_seq:
        result = api_get(f'/select_gender_category/{gc_seq}')
        success = 'result' in result
        print_test('ID로 성별 카테고리 조회', success)
        
        result = api_delete(f'/delete_gender_category/{gc_seq}')
        success = result.get('result') == 'OK'
        print_test('성별 카테고리 삭제', success)


# ============================================
# Product 테스트
# ============================================
def test_product():
    print_header('Product API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_products')
    success = 'results' in result
    print_test('전체 제품 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 카테고리 및 제조사 조회 (필수)
    kind_result = api_get('/select_kind_categories')
    color_result = api_get('/select_color_categories')
    size_result = api_get('/select_size_categories')
    gender_result = api_get('/select_gender_categories')
    maker_result = api_get('/select_makers')
    
    if (kind_result.get('results') and color_result.get('results') and 
        size_result.get('results') and gender_result.get('results') and maker_result.get('results')):
        
        kc_seq = kind_result['results'][0]['kc_seq']
        cc_seq = color_result['results'][0]['cc_seq']
        sc_seq = size_result['results'][0]['sc_seq']
        gc_seq = gender_result['results'][0]['gc_seq']
        m_seq = maker_result['results'][0]['m_seq']
        
        # 3. 제품 추가
        new_product = {
            'kc_seq': kc_seq,
            'cc_seq': cc_seq,
            'sc_seq': sc_seq,
            'gc_seq': gc_seq,
            'm_seq': m_seq,
            'p_name': '테스트제품',
            'p_price': '100000',
            'p_stock': '50',
            'p_image': '/images/test.jpg'
        }
        result = api_post_form('/insert_product', new_product)
        product_seq = result.get('p_seq')
        success = result.get('result') == 'OK' and product_seq is not None
        print_test('제품 추가', success, f"p_seq: {product_seq}")
        
        # 4. ID로 조회
        if product_seq:
            result = api_get(f'/select_product/{product_seq}')
            success = 'result' in result
            print_test('ID로 제품 조회', success)
        
        # 5. 제품 수정
        if product_seq:
            update_data = {
                'p_seq': product_seq,
                'kc_seq': kc_seq,
                'cc_seq': cc_seq,
                'sc_seq': sc_seq,
                'gc_seq': gc_seq,
                'm_seq': m_seq,
                'p_name': '수정된제품',
                'p_price': '120000',
                'p_stock': '60',
                'p_image': '/images/updated.jpg'
            }
            result = api_post_form('/update_product', update_data)
            success = result.get('result') == 'OK'
            print_test('제품 수정', success)
        
        # 6. 재고 수정
        if product_seq:
            result = api_post_form(f'/update_product_stock/{product_seq}', {'p_stock': '70'})
            success = result.get('result') == 'OK'
            print_test('제품 재고 수정', success)
        
        # 7. 제품 삭제
        if product_seq:
            result = api_delete(f'/delete_product/{product_seq}')
            success = result.get('result') == 'OK'
            print_test('제품 삭제', success)


# ============================================
# PurchaseItem 테스트
# ============================================
def test_purchase_item():
    print_header('PurchaseItem API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_purchase_items')
    success = 'results' in result
    print_test('전체 구매 내역 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 필수 데이터 조회
    branch_result = api_get('/select_branches')
    user_result = api_get('/select_users')
    product_result = api_get('/select_products')
    
    if (branch_result.get('results') and user_result.get('results') and product_result.get('results')):
        br_seq = branch_result['results'][0]['br_seq']
        u_seq = user_result['results'][0]['u_seq']
        p_seq = product_result['results'][0]['p_seq']
        
        # 3. 구매 내역 추가
        from datetime import datetime
        new_purchase = {
            'br_seq': br_seq,
            'u_seq': u_seq,
            'p_seq': p_seq,
            'b_price': '150000',
            'b_quantity': '2',
            'b_date': datetime.now().isoformat(),
            'b_tnum': f'TXN{random.randint(1000, 9999)}'
        }
        result = api_post_form('/insert_purchase_item', new_purchase)
        purchase_seq = result.get('b_seq')
        success = result.get('result') == 'OK' and purchase_seq is not None
        print_test('구매 내역 추가', success, f"b_seq: {purchase_seq}")
        
        # 4. ID로 조회
        if purchase_seq:
            result = api_get(f'/select_purchase_item/{purchase_seq}')
            success = 'result' in result
            print_test('ID로 구매 내역 조회', success)
        
        # 5. 고객별 조회
        if u_seq:
            result = api_get(f'/select_purchase_items_by_user/{u_seq}')
            success = 'results' in result
            print_test('고객별 구매 내역 조회', success)
        
        # 6. 구매 내역 삭제
        if purchase_seq:
            result = api_delete(f'/delete_purchase_item/{purchase_seq}')
            success = result.get('result') == 'OK'
            print_test('구매 내역 삭제', success)


# ============================================
# JOIN API 테스트
# ============================================
def test_product_join():
    print_header('Product JOIN API 테스트')
    
    # 제품 조회
    product_result = api_get('/select_products')
    if product_result.get('results'):
        product_seq = product_result['results'][0]['p_seq']
        
        # 제품 전체 상세 조회
        result = api_get(f'/products/{product_seq}/full_detail')
        success = 'result' in result
        print_test('제품 전체 상세 조회', success)
        
        # 제품 목록 + 카테고리 조회
        result = api_get('/products/with_categories')
        success = 'results' in result
        print_test('제품 목록 + 카테고리 조회', success)


def test_purchase_item_join():
    print_header('PurchaseItem JOIN API 테스트')
    
    # 구매 내역 조회
    purchase_result = api_get('/select_purchase_items')
    if purchase_result.get('results'):
        purchase_seq = purchase_result['results'][0]['b_seq']
        
        # 구매 내역 전체 상세 조회
        result = api_get(f'/purchase_items/{purchase_seq}/full_detail')
        success = 'result' in result
        print_test('구매 내역 전체 상세 조회', success)
        
        # b_tnum으로 그룹화된 주문 조회
        b_tnum = purchase_result['results'][0].get('b_tnum')
        if b_tnum:
            result = api_get(f'/purchase_items/by_tnum/{b_tnum}/with_details')
            success = 'result' in result
            print_test('주문번호로 그룹화된 주문 조회', success)


# ============================================
# 메인 함수
# ============================================
def main():
    if len(sys.argv) < 2:
        print("사용법: python test_app_new_form.py [테스트할_파일명]")
        print("\n사용 가능한 테스트:")
        print("  - branch")
        print("  - users")
        print("  - staff")
        print("  - maker")
        print("  - kind_category")
        print("  - color_category")
        print("  - size_category")
        print("  - gender_category")
        print("  - product")
        print("  - purchase_item")
        print("  - product_join")
        print("  - purchase_item_join")
        print("\n예시: python test_app_new_form.py branch")
        return
    
    test_name = sys.argv[1]
    
    test_functions = {
        'branch': test_branch,
        'users': test_users,
        'staff': test_staff,
        'maker': test_maker,
        'kind_category': test_kind_category,
        'color_category': test_color_category,
        'size_category': test_size_category,
        'gender_category': test_gender_category,
        'product': test_product,
        'purchase_item': test_purchase_item,
        'product_join': test_product_join,
        'purchase_item_join': test_purchase_item_join,
    }
    
    if test_name not in test_functions:
        print(f"❌ 알 수 없는 테스트: {test_name}")
        return
    
    test_functions[test_name]()
    
    # 결과 출력
    print('\n' + '=' * 60)
    print('📊 테스트 결과 요약')
    print('=' * 60)
    print(f"✅ 성공: {test_results['passed']}개")
    print(f"❌ 실패: {test_results['failed']}개")
    print(f"📈 성공률: {test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100:.1f}%" if (test_results['passed'] + test_results['failed']) > 0 else "0%")


if __name__ == "__main__":
    main()

