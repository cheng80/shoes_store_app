"""
app_new_form 전체 테스트 자동 실행 스크립트

모든 파일을 순차적으로 서버 실행 → 테스트 → 종료를 반복합니다.
"""

import subprocess
import time
import httpx
import os
import signal
import sys
import random
from datetime import datetime

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
# 테스트 함수들 (간소화 버전)
# ============================================
def test_branch():
    print_header('Branch API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    uid = random.randint(10000, 99999)
    
    r = api_get('/select_branches')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '전체 조회', 'success': s})
    
    r = api_post_form('/insert_branch', {'br_name': f'테스트{uid}', 'br_phone': f'02-{uid}-0000'})
    bid = r.get('br_seq')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {bid}")
    results['passed' if s else 'failed'] += 1
    results['tests'].append({'name': '추가', 'success': s})
    
    if bid:
        r = api_get(f'/select_branch/{bid}')
        s = print_test('ID 조회', 'result' in r)
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': 'ID 조회', 'success': s})
        
        r = api_delete(f'/delete_branch/{bid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
        results['tests'].append({'name': '삭제', 'success': s})
    
    return results


def test_users():
    print_header('Users API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    uid = random.randint(10000, 99999)
    
    r = api_get('/select_users')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    
    r = api_post_form_with_file('/insert_user', {'u_id': f'user{uid}', 'u_password': 'pass', 'u_name': '테스트', 'u_phone': f'010-{uid}-1111'})
    uid_seq = r.get('u_seq')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {uid_seq}")
    results['passed' if s else 'failed'] += 1
    
    if uid_seq:
        r = api_get(f'/select_user/{uid_seq}')
        s = print_test('ID 조회', 'result' in r)
        results['passed' if s else 'failed'] += 1
        
        r = api_delete(f'/delete_user/{uid_seq}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
    
    return results


def test_maker():
    print_header('Maker API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    uid = random.randint(10000, 99999)
    
    r = api_get('/select_makers')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    
    r = api_post_form('/insert_maker', {'m_name': f'테스트{uid}'})
    mid = r.get('m_seq')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {mid}")
    results['passed' if s else 'failed'] += 1
    
    if mid:
        r = api_get(f'/select_maker/{mid}')
        s = print_test('ID 조회', 'result' in r)
        results['passed' if s else 'failed'] += 1
        
        r = api_delete(f'/delete_maker/{mid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
    
    return results


def test_kind_category():
    print_header('KindCategory API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    uid = random.randint(10000, 99999)
    
    r = api_get('/select_kind_categories')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    
    r = api_post_form('/insert_kind_category', {'kc_name': f'테스트{uid}'})
    kcid = r.get('kc_seq')
    s = print_test('추가', r.get('result') == 'OK', f"ID: {kcid}")
    results['passed' if s else 'failed'] += 1
    
    if kcid:
        r = api_get(f'/select_kind_category/{kcid}')
        s = print_test('ID 조회', 'result' in r)
        results['passed' if s else 'failed'] += 1
        
        r = api_delete(f'/delete_kind_category/{kcid}')
        s = print_test('삭제', r.get('result') == 'OK')
        results['passed' if s else 'failed'] += 1
    
    return results


def test_product():
    print_header('Product API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_products')
    s = print_test('전체 조회', 'results' in r, f"{len(r.get('results', []))}건")
    results['passed' if s else 'failed'] += 1
    
    # 카테고리 및 제조사 조회
    kc_r = api_get('/select_kind_categories')
    cc_r = api_get('/select_color_categories')
    sc_r = api_get('/select_size_categories')
    gc_r = api_get('/select_gender_categories')
    m_r = api_get('/select_makers')
    
    if all([kc_r.get('results'), cc_r.get('results'), sc_r.get('results'), gc_r.get('results'), m_r.get('results')]):
        kc_seq = kc_r['results'][0]['kc_seq']
        cc_seq = cc_r['results'][0]['cc_seq']
        sc_seq = sc_r['results'][0]['sc_seq']
        gc_seq = gc_r['results'][0]['gc_seq']
        m_seq = m_r['results'][0]['m_seq']
        
        r = api_post_form('/insert_product', {
            'kc_seq': kc_seq, 'cc_seq': cc_seq, 'sc_seq': sc_seq,
            'gc_seq': gc_seq, 'm_seq': m_seq, 'p_name': '테스트', 'p_price': '100000', 'p_stock': '10'
        })
        pid = r.get('p_seq')
        s = print_test('추가', r.get('result') == 'OK', f"ID: {pid}")
        results['passed' if s else 'failed'] += 1
        
        if pid:
            r = api_get(f'/select_product/{pid}')
            s = print_test('ID 조회', 'result' in r)
            results['passed' if s else 'failed'] += 1
    
    return results


def test_product_join():
    print_header('Product JOIN API')
    results = {'passed': 0, 'failed': 0, 'tests': []}
    
    r = api_get('/select_products')
    if r.get('results'):
        pid = r['results'][0]['p_seq']
        r = api_get(f'/products/{pid}/full_detail')
        s = print_test('제품 전체 상세', 'result' in r)
        results['passed' if s else 'failed'] += 1
        
        r = api_get('/products/with_categories')
        s = print_test('제품 목록 + 카테고리', 'results' in r)
        results['passed' if s else 'failed'] += 1
    
    return results


# ============================================
# 메인 실행
# ============================================
def main():
    print("=" * 60)
    print("🚀 app_new_form 전체 테스트 시작")
    print("=" * 60)
    
    test_files = [
        ('branch.py', test_branch),
        ('maker.py', test_maker),
        ('kind_category.py', test_kind_category),
        ('users.py', test_users),
        ('product.py', test_product),
        ('product_join.py', test_product_join),
    ]
    
    total_passed = 0
    total_failed = 0
    
    for filename, test_func in test_files:
        results = run_server_and_test(filename, test_func)
        total_passed += results['passed']
        total_failed += results['failed']
        all_results[filename] = results
    
    # 최종 결과
    print("\n" + "=" * 60)
    print("📊 전체 테스트 결과")
    print("=" * 60)
    print(f"✅ 성공: {total_passed}개")
    print(f"❌ 실패: {total_failed}개")
    total = total_passed + total_failed
    if total > 0:
        print(f"📈 성공률: {total_passed / total * 100:.1f}%")
    
    print("\n📋 파일별 상세 결과:")
    for filename, results in all_results.items():
        print(f"   {filename}: ✅ {results['passed']}개 / ❌ {results['failed']}개")


if __name__ == "__main__":
    main()

