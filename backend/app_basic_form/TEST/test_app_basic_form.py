"""
app_basic_form API 테스트 스크립트

각 파일을 개별 실행 후 이 스크립트로 테스트합니다.

사용법:
    1. 테스트할 파일 실행: python customers.py
    2. 테스트 실행: python TEST/test_app_basic_form.py customers

작성일: 2025-12-27
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
# Customers 테스트
# ============================================
def test_customers():
    print_header('Customers API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_customers')
    success = 'results' in result
    print_test('전체 고객 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 고객 추가 (이미지 포함 필수)
    uid = random.randint(10000, 99999)
    new_customer = {
        'cEmail': f'test_basic{uid}@test.com',
        'cPhoneNumber': f'010-{uid}-9999',
        'cName': '테스트고객',
        'cPassword': 'testpass'
    }
    result = api_post_form_with_file('/insert_customer', new_customer, 'dummy.png')
    customer_id = result.get('id')
    success = result.get('result') == 'OK' and customer_id is not None
    print_test('고객 추가 (이미지 포함)', success, f"ID: {customer_id}")
    
    # 3. ID로 조회
    if customer_id:
        result = api_get(f'/select_customer/{customer_id}')
        success = result.get('result', {}).get('cEmail') == 'test_basic@test.com'
        print_test('ID로 고객 조회', success)
    
    # 4. 고객 수정 (이미지 제외)
    if customer_id:
        update_data = {
            'customer_id': customer_id,
            'cEmail': f'updated{uid}@test.com',
            'cPhoneNumber': f'010-{uid}-8888',
            'cName': '수정된고객',
            'cPassword': 'newpass'
        }
        result = api_post_form('/update_customer', update_data)
        success = result.get('result') == 'OK'
        print_test('고객 수정 (이미지 제외)', success)
    
    # 4-2. 고객 수정 (이미지 포함)
    if customer_id:
        update_data = {
            'customer_id': customer_id,
            'cEmail': f'updated_img{uid}@test.com',
            'cPhoneNumber': f'010-{uid}-7777',
            'cName': '이미지수정고객',
            'cPassword': 'newpass'
        }
        result = api_post_form_with_file('/update_customer_with_image', update_data, 'dummy.png')
        success = result.get('result') == 'OK'
        print_test('고객 수정 (이미지 포함)', success)
    
    # 4-3. 프로필 이미지 조회
    if customer_id:
        try:
            response = httpx.get(f'{BASE_URL}/view_customer_profile_image/{customer_id}', timeout=10)
            success = response.status_code == 200 and response.headers.get('content-type', '').startswith('image/')
            print_test('프로필 이미지 조회', success)
        except Exception as e:
            print_test('프로필 이미지 조회', False, str(e))
    
    # 5. 수정 확인
    if customer_id:
        result = api_get(f'/select_customer/{customer_id}')
        success = result.get('result', {}).get('cName') == '이미지수정고객'
        print_test('수정 확인', success)
    
    # 6. 고객 삭제
    if customer_id:
        result = api_delete(f'/delete_customer/{customer_id}')
        success = result.get('result') == 'OK'
        print_test('고객 삭제', success)
    
    # 7. 삭제 확인
    if customer_id:
        result = api_get(f'/select_customer/{customer_id}')
        success = 'not found' in result.get('message', '').lower() or result.get('result') == 'Error'
        print_test('삭제 확인', success)


# ============================================
# Employees 테스트
# ============================================
def test_employees():
    print_header('Employees API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_employees')
    success = 'results' in result
    print_test('전체 직원 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 직원 추가 (이미지 포함 필수)
    uid = random.randint(10000, 99999)
    new_emp = {
        'eEmail': f'emp_test{uid}@store.com',
        'ePhoneNumber': f'02-{uid}-2222',
        'eName': '테스트직원',
        'ePassword': 'emppass',
        'eRole': '1'
    }
    result = api_post_form_with_file('/insert_employee', new_emp, 'dummy.png')
    emp_id = result.get('id')
    success = result.get('result') == 'OK' and emp_id is not None
    print_test('직원 추가 (이미지 포함)', success, f"ID: {emp_id}")
    
    # 3. ID로 조회
    if emp_id:
        result = api_get(f'/select_employee/{emp_id}')
        success = result.get('result', {}).get('eEmail') == f'emp_test{uid}@store.com'
        print_test('ID로 직원 조회', success)
    
    # 4. 직원 수정 (이미지 제외)
    if emp_id:
        update_data = {
            'employee_id': emp_id,
            'eEmail': f'emp_updated{uid}@store.com',
            'ePhoneNumber': f'02-{uid}-4444',
            'eName': '수정된직원',
            'ePassword': 'newemppass',
            'eRole': '2'
        }
        result = api_post_form('/update_employee', update_data)
        success = result.get('result') == 'OK'
        print_test('직원 수정 (이미지 제외)', success)
    
    # 4-2. 직원 수정 (이미지 포함)
    if emp_id:
        update_data = {
            'employee_id': emp_id,
            'eEmail': f'emp_img{uid}@store.com',
            'ePhoneNumber': f'02-{uid}-5555',
            'eName': '이미지수정직원',
            'ePassword': 'newemppass',
            'eRole': '2'
        }
        result = api_post_form_with_file('/update_employee_with_image', update_data, 'dummy.png')
        success = result.get('result') == 'OK'
        print_test('직원 수정 (이미지 포함)', success)
    
    # 4-3. 프로필 이미지 조회
    if emp_id:
        try:
            response = httpx.get(f'{BASE_URL}/view_employee_profile_image/{emp_id}', timeout=10)
            success = response.status_code == 200 and response.headers.get('content-type', '').startswith('image/')
            print_test('프로필 이미지 조회', success)
        except Exception as e:
            print_test('프로필 이미지 조회', False, str(e))
    
    # 5. 직원 삭제
    if emp_id:
        result = api_delete(f'/delete_employee/{emp_id}')
        success = result.get('result') == 'OK'
        print_test('직원 삭제', success)


# ============================================
# Manufacturers 테스트
# ============================================
def test_manufacturers():
    print_header('Manufacturers API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_manufacturers')
    success = 'results' in result
    print_test('전체 제조사 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. 제조사 추가
    result = api_post_form('/insert_manufacturer', {'mName': 'TestBrand'})
    mf_id = result.get('id')
    success = result.get('result') == 'OK' and mf_id is not None
    print_test('제조사 추가', success, f"ID: {mf_id}")
    
    # 3. ID로 조회
    if mf_id:
        result = api_get(f'/select_manufacturer/{mf_id}')
        success = result.get('result', {}).get('mName') == 'TestBrand'
        print_test('ID로 제조사 조회', success)
    
    # 4. 제조사 삭제
    if mf_id:
        result = api_delete(f'/delete_manufacturer/{mf_id}')
        success = result.get('result') == 'OK'
        print_test('제조사 삭제', success)


# ============================================
# ProductBases 테스트
# ============================================
def test_product_bases():
    print_header('ProductBases API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_product_bases')
    success = 'results' in result
    print_test('전체 ProductBase 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. ProductBase 추가
    pb_data = {
        'pName': '테스트신발',
        'pDescription': '테스트용 신발입니다',
        'pColor': 'Red',
        'pGender': 'Unisex',
        'pStatus': '',
        'pCategory': 'Running',
        'pModelNumber': 'TEST-001'
    }
    result = api_post_form('/insert_product_base', pb_data)
    pb_id = result.get('id')
    success = result.get('result') == 'OK' and pb_id is not None
    print_test('ProductBase 추가', success, f"ID: {pb_id}")
    
    # 3. ID로 조회
    if pb_id:
        result = api_get(f'/select_product_base/{pb_id}')
        success = result.get('result', {}).get('pName') == '테스트신발'
        print_test('ID로 ProductBase 조회', success)
    
    # 4. ProductBase 삭제
    if pb_id:
        result = api_delete(f'/delete_product_base/{pb_id}')
        success = result.get('result') == 'OK'
        print_test('ProductBase 삭제', success)


# ============================================
# ProductImages 테스트
# ============================================
def test_product_images():
    print_header('ProductImages API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_product_images')
    success = 'results' in result
    print_test('전체 ProductImage 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. ProductImage 추가 (pbid=1 가정)
    result = api_post_form('/insert_product_image', {'pbid': 1, 'imagePath': 'test/image.png'})
    img_id = result.get('id')
    success = result.get('result') == 'OK' and img_id is not None
    print_test('ProductImage 추가', success, f"ID: {img_id}")
    
    # 3. pbid로 조회
    result = api_get('/select_product_images_by_pbid/1')
    success = 'results' in result
    print_test('pbid로 ProductImage 조회', success)
    
    # 4. ProductImage 삭제
    if img_id:
        result = api_delete(f'/delete_product_image/{img_id}')
        success = result.get('result') == 'OK'
        print_test('ProductImage 삭제', success)


# ============================================
# Products 테스트
# ============================================
def test_products():
    print_header('Products API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_products')
    success = 'results' in result
    print_test('전체 Product 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. Product 추가 (pbid=1, mfid=1 가정)
    prod_data = {
        'pbid': 1,
        'mfid': 1,
        'size': 265,
        'basePrice': 99000,
        'pQuantity': 10
    }
    result = api_post_form('/insert_product', prod_data)
    prod_id = result.get('id')
    success = result.get('result') == 'OK' and prod_id is not None
    print_test('Product 추가', success, f"ID: {prod_id}")
    
    # 3. pbid로 조회
    result = api_get('/select_products_by_pbid/1')
    success = 'results' in result
    print_test('pbid로 Product 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 4. ID로 조회
    if prod_id:
        result = api_get(f'/select_product/{prod_id}')
        success = result.get('result', {}).get('size') == 265
        print_test('ID로 Product 조회', success)
    
    # 5. Product 삭제
    if prod_id:
        result = api_delete(f'/delete_product/{prod_id}')
        success = result.get('result') == 'OK'
        print_test('Product 삭제', success)


# ============================================
# Purchases 테스트
# ============================================
def test_purchases():
    print_header('Purchases API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_purchases')
    success = 'results' in result
    print_test('전체 Purchase 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. Purchase 추가 (cid=1 가정)
    purchase_data = {
        'cid': 1,
        'pickupDate': '2025-12-30 14:00',
        'orderCode': 'TEST-ORDER-001',
        'timeStamp': '2025-12-27 12:00'
    }
    result = api_post_form('/insert_purchase', purchase_data)
    purchase_id = result.get('id')
    success = result.get('result') == 'OK' and purchase_id is not None
    print_test('Purchase 추가', success, f"ID: {purchase_id}")
    
    # 3. cid로 조회
    result = api_get('/select_purchases_by_cid/1')
    success = 'results' in result
    print_test('cid로 Purchase 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 4. ID로 조회
    if purchase_id:
        result = api_get(f'/select_purchase/{purchase_id}')
        success = result.get('result', {}).get('orderCode') == 'TEST-ORDER-001'
        print_test('ID로 Purchase 조회', success)
    
    # 5. Purchase 삭제
    if purchase_id:
        result = api_delete(f'/delete_purchase/{purchase_id}')
        success = result.get('result') == 'OK'
        print_test('Purchase 삭제', success)


# ============================================
# PurchaseItems 테스트
# ============================================
def test_purchase_items():
    print_header('PurchaseItems API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_purchase_items')
    success = 'results' in result
    print_test('전체 PurchaseItem 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. PurchaseItem 추가 (pid=1, pcid=1 가정)
    item_data = {
        'pid': 1,
        'pcid': 1,
        'pcQuantity': 2,
        'pcStatus': '제품 준비 중'
    }
    result = api_post_form('/insert_purchase_item', item_data)
    item_id = result.get('id')
    success = result.get('result') == 'OK' and item_id is not None
    print_test('PurchaseItem 추가', success, f"ID: {item_id}")
    
    # 3. pcid로 조회
    result = api_get('/select_purchase_items_by_pcid/1')
    success = 'results' in result
    print_test('pcid로 PurchaseItem 조회', success)
    
    # 4. PurchaseItem 삭제
    if item_id:
        result = api_delete(f'/delete_purchase_item/{item_id}')
        success = result.get('result') == 'OK'
        print_test('PurchaseItem 삭제', success)


# ============================================
# LoginHistories 테스트
# ============================================
def test_login_histories():
    print_header('LoginHistories API 테스트')
    
    # 1. 전체 조회
    result = api_get('/select_login_histories')
    success = 'results' in result
    print_test('전체 LoginHistory 조회', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. LoginHistory 추가 (cid=1 가정)
    login_data = {
        'cid': 1,
        'loginTime': '2025-12-27 12:00',
        'lStatus': 'active',
        'lVersion': 1.0,
        'lAddress': '테스트주소',
        'lPaymentMethod': 'Card'
    }
    result = api_post_form('/insert_login_history', login_data)
    login_id = result.get('id')
    success = result.get('result') == 'OK' and login_id is not None
    print_test('LoginHistory 추가', success, f"ID: {login_id}")
    
    # 3. cid로 조회
    result = api_get('/select_login_histories_by_cid/1')
    success = 'results' in result
    print_test('cid로 LoginHistory 조회', success)
    
    # 4. LoginHistory 삭제
    if login_id:
        result = api_delete(f'/delete_login_history/{login_id}')
        success = result.get('result') == 'OK'
        print_test('LoginHistory 삭제', success)


# ============================================
# ProductBases JOIN 테스트
# ============================================
def test_product_bases_join():
    print_header('ProductBases JOIN API 테스트')
    
    # 1. with_first_image
    result = api_get('/product_bases/with_first_image')
    success = 'results' in result
    print_test('ProductBase + 첫이미지', success, f"조회: {len(result.get('results', []))}건")
    
    # 2. with_images (pbid=1)
    result = api_get('/product_bases/1/with_images')
    success = 'result' in result and 'images' in result.get('result', {})
    print_test('ProductBase + 전체이미지', success)
    
    # 3. with_products (pbid=1)
    result = api_get('/product_bases/1/with_products')
    success = 'result' in result and 'products' in result.get('result', {})
    print_test('ProductBase + Products', success)
    
    # 4. full_detail (4테이블 JOIN)
    result = api_get('/product_bases/full_detail')
    success = 'results' in result
    if success and result['results']:
        first = result['results'][0]
        has_all = 'firstImage' in first and 'representativeProduct' in first and 'manufacturer' in first
        print_test('ProductBase 전체상세 (4테이블)', has_all, f"조회: {len(result['results'])}건")
    else:
        print_test('ProductBase 전체상세 (4테이블)', success)


# ============================================
# Products JOIN 테스트
# ============================================
def test_products_join():
    print_header('Products JOIN API 테스트')
    
    # 1. with_base
    result = api_get('/products/1/with_base')
    success = 'result' in result and 'productBase' in result.get('result', {})
    print_test('Product + ProductBase', success)
    
    # 2. with_base_and_manufacturer
    result = api_get('/products/1/with_base_and_manufacturer')
    success = 'result' in result
    if success:
        r = result.get('result', {})
        has_all = 'productBase' in r and 'manufacturer' in r
        print_test('Product + ProductBase + Manufacturer', has_all)
    else:
        print_test('Product + ProductBase + Manufacturer', False)
    
    # 3. by_pbid with_base
    result = api_get('/products/by_pbid/1/with_base')
    success = 'productBase' in result and 'products' in result
    print_test('Products by pbid + ProductBase', success)
    
    # 4. full_detail
    result = api_get('/products/1/full_detail')
    success = 'result' in result
    if success:
        r = result.get('result', {})
        has_all = 'productBase' in r and 'manufacturer' in r and 'images' in r
        print_test('Product 전체상세', has_all)
    else:
        print_test('Product 전체상세', False)


# ============================================
# Purchases JOIN 테스트
# ============================================
def test_purchases_join():
    print_header('Purchases JOIN API 테스트')
    
    # 1. with_customer (단일)
    result = api_get('/purchases/1/with_customer')
    success = 'result' in result and 'customer' in result.get('result', {})
    print_test('Purchase + Customer', success)
    
    # 2. with_customer (목록)
    result = api_get('/purchases/with_customer?cid=1')
    success = 'results' in result
    print_test('Purchases + Customer (cid별)', success, f"조회: {len(result.get('results', []))}건")
    
    # 3. with_customer (전체)
    result = api_get('/purchases/with_customer')
    success = 'results' in result
    print_test('Purchases + Customer (전체)', success, f"조회: {len(result.get('results', []))}건")
    
    # 4. with_items (단일)
    result = api_get('/purchases/1/with_items')
    success = 'result' in result and 'items' in result.get('result', {})
    print_test('Purchase + Items', success)
    
    # 5. with_items (목록)
    result = api_get('/purchases/with_items?cid=1')
    success = 'results' in result
    print_test('Purchases + Items (cid별)', success)
    
    # 6. full_detail
    result = api_get('/purchases/1/full_detail')
    success = 'result' in result
    if success:
        r = result.get('result', {})
        has_all = 'customer' in r and 'items' in r
        print_test('Purchase 전체상세', has_all)
    else:
        print_test('Purchase 전체상세', False)


# ============================================
# PurchaseItems JOIN 테스트
# ============================================
def test_purchase_items_join():
    print_header('PurchaseItems JOIN API 테스트')
    
    # 1. with_product (단일)
    result = api_get('/purchase_items/1/with_product')
    success = 'result' in result and 'product' in result.get('result', {})
    print_test('PurchaseItem + Product', success)
    
    # 2. by_pcid with_product
    result = api_get('/purchase_items/by_pcid/1/with_product')
    success = 'results' in result
    print_test('PurchaseItems by pcid + Product', success)
    
    # 3. full_detail (단일, 4테이블)
    result = api_get('/purchase_items/1/full_detail')
    success = 'result' in result
    if success:
        r = result.get('result', {})
        has_all = 'productBase' in r and 'manufacturer' in r
        print_test('PurchaseItem 전체상세 (4테이블)', has_all)
    else:
        print_test('PurchaseItem 전체상세 (4테이블)', False)
    
    # 4. by_pcid full_detail
    result = api_get('/purchase_items/by_pcid/1/full_detail')
    success = 'results' in result and 'totalAmount' in result
    print_test('PurchaseItems by pcid 전체상세', success)
    
    # 5. summary
    result = api_get('/purchase_items/summary/1')
    success = 'result' in result
    if success:
        r = result.get('result', {})
        has_all = 'itemCount' in r and 'totalAmount' in r
        print_test('PurchaseItems 요약', has_all)
    else:
        print_test('PurchaseItems 요약', False)


# ============================================
# 결과 요약
# ============================================
def print_summary():
    print('\n' + '=' * 60)
    print('📊 테스트 결과 요약')
    print('=' * 60)
    
    total = test_results['passed'] + test_results['failed']
    pass_rate = (test_results['passed'] / total * 100) if total > 0 else 0
    
    print(f'\n   전체 테스트: {total}개')
    print(f'   ✅ 성공: {test_results["passed"]}개')
    print(f'   ❌ 실패: {test_results["failed"]}개')
    print(f'   📈 성공률: {pass_rate:.1f}%')
    
    failed_tests = [t for t in test_results['tests'] if not t['success']]
    if failed_tests:
        print('\n   --- 실패한 테스트 ---')
        for test in failed_tests:
            print(f'   ❌ {test["name"]}')
    
    print('\n' + '=' * 60)
    if test_results['failed'] == 0:
        print('🎉 모든 테스트가 성공했습니다!')
    else:
        print(f'⚠️ {test_results["failed"]}개의 테스트가 실패했습니다.')
    print('=' * 60)


# ============================================
# 메인
# ============================================
TEST_MODULES = {
    'customers': test_customers,
    'employees': test_employees,
    'manufacturers': test_manufacturers,
    'product_bases': test_product_bases,
    'product_images': test_product_images,
    'products': test_products,
    'purchases': test_purchases,
    'purchase_items': test_purchase_items,
    'login_histories': test_login_histories,
    'product_bases_join': test_product_bases_join,
    'products_join': test_products_join,
    'purchases_join': test_purchases_join,
    'purchase_items_join': test_purchase_items_join,
}


def main():
    if len(sys.argv) < 2:
        print('사용법: python TEST/test_app_basic_form.py <module_name>')
        print('\n사용 가능한 모듈:')
        for name in TEST_MODULES:
            print(f'  - {name}')
        print('\n예시: python TEST/test_app_basic_form.py customers')
        return
    
    module_name = sys.argv[1]
    
    if module_name == 'all':
        print('\n⚠️ 전체 테스트는 각 파일을 개별 실행해야 합니다.')
        print('각 파일을 실행 후 해당 모듈 테스트를 수행하세요.')
        return
    
    if module_name not in TEST_MODULES:
        print(f'❌ 알 수 없는 모듈: {module_name}')
        print('\n사용 가능한 모듈:')
        for name in TEST_MODULES:
            print(f'  - {name}')
        return
    
    print(f'\n🚀 {module_name} 테스트 시작...')
    print(f'   서버: {BASE_URL}')
    
    # 서버 연결 확인
    try:
        httpx.get(BASE_URL, timeout=3)
    except:
        print(f'\n❌ 서버에 연결할 수 없습니다.')
        print(f'   먼저 서버를 실행하세요: python {module_name}.py')
        return
    
    # 테스트 실행
    TEST_MODULES[module_name]()
    
    # 결과 요약
    print_summary()


if __name__ == '__main__':
    main()

