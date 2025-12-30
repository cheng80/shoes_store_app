"""
종합 테스트 실행 스크립트
- 더미 데이터 생성
- main.py 서버 실행
- 모든 API 테스트 실행
"""

import subprocess
import time
import httpx
import os
import sys
import signal
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'http://127.0.0.1:8000'

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

def wait_for_server(timeout=20):
    """서버가 준비될 때까지 대기"""
    start = time.time()
    print(f'   서버 시작 대기 중... (최대 {timeout}초)')
    while time.time() - start < timeout:
        try:
            response = httpx.get(f'{BASE_URL}/health', timeout=2)
            if response.status_code == 200:
                print(f'   서버 준비 완료 ({int(time.time() - start)}초 소요)')
                return True
        except Exception as e:
            if time.time() - start > 5:
                print(f'   대기 중... ({int(time.time() - start)}초 경과)')
        time.sleep(1)
    print(f'   서버 시작 타임아웃 ({timeout}초)')
    return False

def run_comprehensive_test():
    """종합 테스트 실행"""
    print_header('종합 테스트 시작')
    
    # 1. 더미 데이터 생성
    print_header('1. 더미 데이터 생성')
    try:
        dummy_script = os.path.join(BASE_DIR, 'TEST', 'create_dummy_data.py')
        result = subprocess.run(
            [sys.executable, dummy_script],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print_test('더미 데이터 생성', True)
            print(result.stdout)
        else:
            print_test('더미 데이터 생성', False, result.stderr)
            return
    except Exception as e:
        print_test('더미 데이터 생성', False, str(e))
        return
    
    # 2. 서버 시작
    print_header('2. 서버 시작')
    server_proc = None
    try:
        # 상위 디렉토리에서 실행 (backend 디렉토리)
        backend_dir = os.path.dirname(BASE_DIR)
        main_script = os.path.join('app_new_form', 'main.py')
        
        # 환경 변수 설정
        env = os.environ.copy()
        env['PYTHONPATH'] = backend_dir
        
        server_proc = subprocess.Popen(
            [sys.executable, main_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=backend_dir,
            env=env
        )
        
        # 서버 로그 확인을 위한 짧은 대기
        time.sleep(2)
        
        if wait_for_server(timeout=25):
            print_test('서버 시작', True)
        else:
            # 서버 로그 출력
            if server_proc.stdout:
                output = server_proc.stdout.read().decode('utf-8', errors='ignore')
                if output:
                    print(f'   서버 로그:\n{output[:500]}')
            print_test('서버 시작', False, '타임아웃')
            if server_proc:
                server_proc.terminate()
            return
    except Exception as e:
        print_test('서버 시작', False, str(e))
        if server_proc:
            server_proc.terminate()
        return
    
    # 3. API 테스트 실행
    print_header('3. API 테스트 실행')
    test_results = {'passed': 0, 'failed': 0}
    
    try:
        # 기본 엔드포인트 테스트
        tests = [
            ('헬스 체크', '/health'),
            ('루트 엔드포인트', '/'),
            ('지점 목록', '/api/branches'),
            ('고객 목록', '/api/users'),
            ('직원 목록', '/api/staffs'),
            ('제조사 목록', '/api/makers'),
            ('제품 목록', '/api/products'),
            ('구매 내역 목록', '/api/purchase_items'),
            ('수령 목록', '/api/pickups'),
            ('반품 목록', '/api/refunds'),
        ]
        
        for test_name, endpoint in tests:
            result = api_get(endpoint)
            success = 'error' not in result and (result.get('results') is not None or result.get('status') is not None or result.get('message') is not None)
            print_test(test_name, success)
            if success:
                test_results['passed'] += 1
            else:
                test_results['failed'] += 1
        
        # JOIN API 테스트
        print_header('4. JOIN API 테스트')
        join_tests = [
            ('제품 상세 (JOIN)', '/api/products/1/full_detail'),
            ('구매 내역 상세 (JOIN)', '/api/purchase_items/1/with_details'),
            ('고객별 주문 목록', '/api/purchase_items/by_user/1/orders'),
        ]
        
        for test_name, endpoint in join_tests:
            result = api_get(endpoint)
            success = 'error' not in result and ('result' in result or 'results' in result)
            print_test(test_name, success)
            if success:
                test_results['passed'] += 1
            else:
                test_results['failed'] += 1
        
        # 분 단위 그룹핑 테스트
        print_header('5. 분 단위 그룹핑 테스트')
        
        # 구매 내역 조회
        purchase_result = api_get('/api/purchase_items')
        if purchase_result.get('results') and len(purchase_result['results']) > 0:
            first_purchase = purchase_result['results'][0]
            b_date = first_purchase.get('b_date')
            u_seq = first_purchase.get('u_seq')
            br_seq = first_purchase.get('br_seq')
            
            if b_date and u_seq and br_seq:
                # datetime을 YYYY-MM-DD HH:MM 형식으로 변환
                if 'T' in b_date:
                    dt_str = b_date.split('T')[1].split('.')[0]
                    date_part = b_date.split('T')[0]
                    time_part = ':'.join(dt_str.split(':')[:2])
                    order_datetime = f"{date_part} {time_part}"
                else:
                    parts = b_date.split(' ')
                    if len(parts) >= 2:
                        date_part = parts[0]
                        time_part = ':'.join(parts[1].split(':')[:2])
                        order_datetime = f"{date_part} {time_part}"
                    else:
                        order_datetime = b_date
                
                # 분 단위 그룹핑 조회 테스트
                endpoint = f'/api/purchase_items/by_datetime/with_details?user_seq={u_seq}&order_datetime={order_datetime}&branch_seq={br_seq}'
                result = api_get(endpoint)
                success = 'error' not in result and 'result' in result
                print_test('분 단위 주문 그룹핑 조회', success)
                if success:
                    test_results['passed'] += 1
                else:
                    test_results['failed'] += 1
                    print(f'      오류: {result.get("error", result)}')
        
    except Exception as e:
        print_test('테스트 실행 중 오류', False, str(e))
        test_results['failed'] += 1
    
    finally:
        # 서버 종료
        if server_proc:
            print_header('6. 서버 종료')
            server_proc.terminate()
            try:
                server_proc.wait(timeout=3)
                print_test('서버 종료', True)
            except:
                server_proc.kill()
                print_test('서버 강제 종료', True)
            time.sleep(1)
    
    # 최종 결과
    print_header('최종 테스트 결과')
    total = test_results['passed'] + test_results['failed']
    print(f"✅ 성공: {test_results['passed']}개")
    print(f"❌ 실패: {test_results['failed']}개")
    if total > 0:
        print(f"📈 성공률: {test_results['passed'] / total * 100:.1f}%")
    
    return test_results

if __name__ == "__main__":
    run_comprehensive_test()

