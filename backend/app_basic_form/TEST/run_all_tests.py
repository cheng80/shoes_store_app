"""
app_basic_form 전체 테스트 자동 실행 스크립트

모든 파일을 순차적으로 서버 실행 → 테스트 → 종료를 반복합니다.
"""

import subprocess
import time
import httpx
import os
import signal
import sys
import random

# 프로젝트 경로
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'http://127.0.0.1:8000'

# 전체 결과
all_results = {}

# ============================================
# 유틸리티 함수
# ============================================
def print_header(title: str):
    print('\n' + '=' * 60)
    print(f'🧪 {title}')
    print('=' * 60)


def print_test(name: str, success: bool, detail: str = ''):
    icon = '✅' if success else '❌'
    print(f'   {icon} {name}', end='')
    if detail:
        print(f' - {detail}')
    else:
        print()
    return success


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


def api_post_form_with_file(endpoint: str, data: dict) -> dict:
    """Form 데이터와 파일 업로드"""
    try:
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


def wait_for_server(timeout=10):
    """서버가 준비될 때까지 대기"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            httpx.get(BASE_URL, timeout=1)
            return True
        except:
            time.sleep(0.5)
    return False


def run_server_and_test(filename: str, test_func):
    """서버 실행 → 테스트 → 종료"""
    filepath = os.path.join(BASE_DIR, filename)
    
    print(f'\n📂 {filename} 테스트 시작...')
    
    # 서버 시작
    proc = subprocess.Popen(
        [sys.executable, filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=BASE_DIR
    )
    
    # 서버 준비 대기
    if not wait_for_server():
        print(f'   ❌ 서버 시작 실패')
        proc.terminate()
        return {'passed': 0, 'failed': 1, 'tests': [{'name': '서버 시작', 'success': False}]}
    
    # 테스트 실행
    results = test_func()
    
    # 서버 종료
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except:
        proc.kill()
    
    time.sleep(1)  # 포트 해제 대기
    
    return results


# ============================================
# 테스트 함수들
# ============================================
def test_customers():
    print_header('Customers API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    uid = random.randint(10000, 99999)
    
    # 전체 조회
    r = api_get('/select_customers')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    # 추가 (이미지 포함 필수)
    r = api_post_form_with_file('/insert_customer', {'cEmail': f'test{uid}@test.com', 'cPhoneNumber': f'010-{uid}-1111', 'cName': '테스트', 'cPassword': 'pass'})
    cid = r.get('id')
    s = print_test('추가 (이미지 포함)', r.get('result') == 'OK', f"ID: {cid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    # ID 조회
    if cid:
        r = api_get(f'/select_customer/{cid}')
        s = print_test('ID 조회', 'result' in r)
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': 'ID 조회', 'success': s})
    
    # 수정 (이미지 제외)
    if cid:
        r = api_post_form('/update_customer', {'customer_id': str(cid), 'cEmail': f'updated{uid}@test.com', 'cPhoneNumber': f'010-{uid}-2222', 'cName': '수정됨', 'cPassword': 'newpass'})
        s = print_test('수정 (이미지 제외)', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '수정', 'success': s})
    
    # 삭제
    if cid:
        r = api_delete(f'/delete_customer/{cid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_employees():
    print_header('Employees API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_employees')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    uid = random.randint(10000, 99999)
    r = api_post_form_with_file('/insert_employee', {'eEmail': f'emp{uid}@test.com', 'ePhoneNumber': f'02-{uid}-1111', 'eName': '테스트직원', 'ePassword': 'pass', 'eRole': '1'})
    eid = r.get('id')
    s = print_test('추가 (이미지 포함)', r.get('result') == 'OK', f"ID: {eid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if eid:
        r = api_delete(f'/delete_employee/{eid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_manufacturers():
    print_header('Manufacturers API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_manufacturers')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    r = api_post_form('/insert_manufacturer', {'mName': 'TestBrand'})
    mid = r.get('id')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {mid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if mid:
        r = api_delete(f'/delete_manufacturer/{mid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_product_bases():
    print_header('ProductBases API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_product_bases')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    uid = random.randint(10000, 99999)
    r = api_post_form('/insert_product_base', {'pName': f'테스트신발{uid}', 'pDescription': '설명', 'pColor': 'Red', 'pGender': 'Unisex', 'pStatus': 'active', 'pCategory': 'Running', 'pModelNumber': f'TEST-{uid}'})
    pbid = r.get('id')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {pbid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if pbid:
        r = api_delete(f'/delete_product_base/{pbid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_product_images():
    print_header('ProductImages API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_product_images')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    r = api_post_form('/insert_product_image', {'pbid': 1, 'imagePath': 'test/image.png'})
    imgid = r.get('id')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {imgid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    r = api_get('/select_product_images_by_pbid/1')
    s = print_test('pbid로 조회', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'pbid로 조회', 'success': s})
    
    if imgid:
        r = api_delete(f'/delete_product_image/{imgid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_products():
    print_header('Products API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_products')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    r = api_get('/select_products_by_pbid/1')
    s = print_test('pbid로 조회', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'pbid로 조회', 'success': s})
    
    r = api_post_form('/insert_product', {'pbid': 1, 'mfid': 1, 'size': 265, 'basePrice': 99000, 'pQuantity': 10})
    pid = r.get('id')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {pid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if pid:
        r = api_delete(f'/delete_product/{pid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_purchases():
    print_header('Purchases API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_purchases')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    r = api_get('/select_purchases_by_cid/1')
    s = print_test('cid로 조회', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'cid로 조회', 'success': s})
    
    r = api_post_form('/insert_purchase', {'cid': 1, 'pickupDate': '2025-12-30 14:00', 'orderCode': 'TEST-001', 'timeStamp': '2025-12-27 12:00'})
    pcid = r.get('id')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {pcid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if pcid:
        r = api_delete(f'/delete_purchase/{pcid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_purchase_items():
    print_header('PurchaseItems API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_purchase_items')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    r = api_get('/select_purchase_items_by_pcid/1')
    s = print_test('pcid로 조회', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'pcid로 조회', 'success': s})
    
    r = api_post_form('/insert_purchase_item', {'pid': 1, 'pcid': 1, 'pcQuantity': 2, 'pcStatus': '준비중'})
    piid = r.get('id')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {piid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if piid:
        r = api_delete(f'/delete_purchase_item/{piid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_login_histories():
    print_header('LoginHistories API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_login_histories')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    r = api_get('/select_login_histories_by_cid/1')
    s = print_test('cid로 조회', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'cid로 조회', 'success': s})
    
    r = api_post_form('/insert_login_history', {'cid': 1, 'loginTime': '2025-12-27 12:00', 'lStatus': 'active', 'lVersion': 1.0, 'lAddress': '주소', 'lPaymentMethod': 'Card'})
    lid = r.get('id')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {lid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if lid:
        r = api_delete(f'/delete_login_history/{lid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_product_bases_join():
    print_header('ProductBases JOIN API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/product_bases/with_first_image')
    s = print_test('with_first_image', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_first_image', 'success': s})
    
    r = api_get('/product_bases/1/with_images')
    s = print_test('with_images', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_images', 'success': s})
    
    r = api_get('/product_bases/1/with_products')
    s = print_test('with_products', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_products', 'success': s})
    
    r = api_get('/product_bases/full_detail')
    s = print_test('full_detail (4테이블)', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'full_detail', 'success': s})
    
    return results


def test_products_join():
    print_header('Products JOIN API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/products/1/with_base')
    s = print_test('with_base', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_base', 'success': s})
    
    r = api_get('/products/1/with_base_and_manufacturer')
    s = print_test('with_base_and_manufacturer', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_base_and_manufacturer', 'success': s})
    
    r = api_get('/products/by_pbid/1/with_base')
    s = print_test('by_pbid/with_base', 'products' in r or 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'by_pbid/with_base', 'success': s})
    
    r = api_get('/products/1/full_detail')
    s = print_test('full_detail', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'full_detail', 'success': s})
    
    return results


def test_purchases_join():
    print_header('Purchases JOIN API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/purchases/1/with_customer')
    s = print_test('with_customer', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_customer', 'success': s})
    
    r = api_get('/purchases/with_customer?cid=1')
    s = print_test('with_customer (cid)', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_customer (cid)', 'success': s})
    
    r = api_get('/purchases/with_customer')
    s = print_test('with_customer (전체)', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_customer (전체)', 'success': s})
    
    r = api_get('/purchases/1/with_items')
    s = print_test('with_items', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_items', 'success': s})
    
    r = api_get('/purchases/with_items?cid=1')
    s = print_test('with_items (cid)', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_items (cid)', 'success': s})
    
    r = api_get('/purchases/1/full_detail')
    s = print_test('full_detail', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'full_detail', 'success': s})
    
    return results


def test_purchase_items_join():
    print_header('PurchaseItems JOIN API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/purchase_items/1/with_product')
    s = print_test('with_product', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'with_product', 'success': s})
    
    r = api_get('/purchase_items/by_pcid/1/with_product')
    s = print_test('by_pcid/with_product', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'by_pcid/with_product', 'success': s})
    
    r = api_get('/purchase_items/1/full_detail')
    s = print_test('full_detail (4테이블)', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'full_detail', 'success': s})
    
    r = api_get('/purchase_items/by_pcid/1/full_detail')
    s = print_test('by_pcid/full_detail', 'results' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'by_pcid/full_detail', 'success': s})
    
    r = api_get('/purchase_items/summary/1')
    s = print_test('summary', 'result' in r)
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': 'summary', 'success': s})
    
    return results


# ============================================
# 메인 실행
# ============================================
def main():
    print('\n' + '🚀' * 20)
    print('\n   app_basic_form 전체 테스트')
    print('\n' + '🚀' * 20)
    
    # 단일 CRUD 테스트
    test_files = [
        ('customers.py', test_customers),
        ('employees.py', test_employees),
        ('manufacturers.py', test_manufacturers),
        ('product_bases.py', test_product_bases),
        ('product_images.py', test_product_images),
        ('products.py', test_products),
        ('purchases.py', test_purchases),
        ('purchase_items.py', test_purchase_items),
        ('login_histories.py', test_login_histories),
        ('product_bases_join.py', test_product_bases_join),
        ('products_join.py', test_products_join),
        ('purchases_join.py', test_purchases_join),
        ('purchase_items_join.py', test_purchase_items_join),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for filename, test_func in test_files:
        results = run_server_and_test(filename, test_func)
        all_results[filename] = results
        total_passed += results['passed']
        total_failed += results['failed']
    
    # 최종 요약
    print('\n' + '=' * 60)
    print('📊 전체 테스트 결과 요약')
    print('=' * 60)
    
    for filename, results in all_results.items():
        icon = '✅' if results['failed'] == 0 else '⚠️'
        print(f'   {icon} {filename}: {results["passed"]}개 성공, {results["failed"]}개 실패')
    
    print('\n' + '-' * 60)
    total = total_passed + total_failed
    rate = (total_passed / total * 100) if total > 0 else 0
    print(f'   전체 테스트: {total}개')
    print(f'   ✅ 성공: {total_passed}개')
    print(f'   ❌ 실패: {total_failed}개')
    print(f'   📈 성공률: {rate:.1f}%')
    print('=' * 60)
    
    if total_failed == 0:
        print('🎉 모든 테스트가 성공했습니다!')
    else:
        print(f'⚠️ {total_failed}개의 테스트가 실패했습니다.')
    
    return all_results


if __name__ == '__main__':
    results = main()

