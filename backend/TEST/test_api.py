"""
API 테스트 스크립트

이 스크립트는 FastAPI 백엔드의 모든 API를 테스트합니다.
회원가입, 로그인, 주문, 반품 등의 시나리오를 포함합니다.

사용법:
    1. 가상환경 활성화: source venv/bin/activate
    2. 서버 실행: uvicorn app.main:app --host 127.0.0.1 --port 8000
    3. 테스트 실행: python TEST/test_api.py

작성일: 2025-12-25

============================================
📋 API 분류
============================================

1. 기본 CRUD API
   - GET, POST, PUT, DELETE 기본 동작

2. JOIN API (복합 쿼리)
   - 여러 테이블을 조인하여 한번에 조회

3. 필터링 API
   - 쿼리 파라미터로 조건부 조회
   - 예: /customers?email=... , /employees?role=...

4. 부분 업데이트 API (PATCH)
   - 특정 필드만 업데이트
   - 예: /login_histories/by_customer/{cid}/status

============================================
🚀 최적화 API (N번 호출 → 1번 호출)
============================================

Flutter 앱에서 여러 핸들러를 순차 호출하던 패턴을
1번의 API 호출로 대체할 수 있는 통합 API들:

1. GET /api/product_bases/list/full_detail
   - 용도: 검색/제품 목록 화면
   - 기존: ProductBase조회 + Product조회×N + Manufacturer조회×N
   - 개선: 1번 호출로 ProductBase + 첫이미지 + 대표Product + Manufacturer 통합 조회
   - 성능: 25회 → 1회 (96% 감소)

2. GET /api/purchases/list/with_items
   - 용도: 주문 목록 화면
   - 기존: Purchase조회 + PurchaseItem조회×N
   - 개선: 1번 호출로 Purchase목록 + 각 주문의 PurchaseItem 목록 포함
   - 성능: 6회 → 1회 (83% 감소)

3. GET /api/purchases/list/with_customer (cid 없이)
   - 용도: 관리자 주문 관리 화면
   - 기존: Purchase전체조회 + Customer조회×N
   - 개선: 1번 호출로 전체 Purchase + Customer 정보 통합 조회
   - 성능: 11회 → 1회 (91% 감소)
"""

import httpx
import json
from typing import Optional

# ============================================
# 설정
# ============================================

# API 기본 URL
BASE_URL = 'http://127.0.0.1:8000/api'

# 테스트 결과 저장용
test_results = {
    'passed': 0,
    'failed': 0,
    'tests': []
}


# ============================================
# 유틸리티 함수
# ============================================

def print_header(title: str):
    """테스트 섹션 헤더 출력"""
    print('\n' + '=' * 60)
    print(f'🧪 {title}')
    print('=' * 60)


def print_test(name: str, success: bool, detail: str = ''):
    """테스트 결과 출력 및 저장"""
    icon = '✅' if success else '❌'
    print(f'   {icon} {name}')
    if detail:
        print(f'      {detail}')
    
    # 결과 저장
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
    """GET 요청 헬퍼 함수"""
    response = httpx.get(f'{BASE_URL}{endpoint}')
    return response.json()


def api_post(endpoint: str, data: dict) -> dict:
    """POST 요청 헬퍼 함수"""
    response = httpx.post(f'{BASE_URL}{endpoint}', json=data)
    return response.json()


def api_put(endpoint: str, data: dict) -> dict:
    """PUT 요청 헬퍼 함수"""
    response = httpx.put(f'{BASE_URL}{endpoint}', json=data)
    return response.json()


def api_delete(endpoint: str) -> dict:
    """DELETE 요청 헬퍼 함수"""
    response = httpx.delete(f'{BASE_URL}{endpoint}')
    return response.json()


def api_patch(endpoint: str) -> dict:
    """PATCH 요청 헬퍼 함수 (쿼리 파라미터용)"""
    response = httpx.patch(f'{BASE_URL}{endpoint}')
    return response.json()


# ============================================
# 테스트 1: 헬스 체크
# ============================================

def test_health_check():
    """서버 상태 및 DB 연결 확인"""
    print_header('헬스 체크')
    
    try:
        response = httpx.get('http://127.0.0.1:8000/health')
        result = response.json()
        
        # 서버 상태 확인
        is_healthy = result.get('status') == 'healthy'
        print_test('서버 상태', is_healthy, f"status: {result.get('status')}")
        
        # DB 연결 확인
        is_db_connected = result.get('database') == 'connected'
        print_test('DB 연결', is_db_connected, f"database: {result.get('database')}")
        
        return is_healthy and is_db_connected
    except Exception as e:
        print_test('헬스 체크', False, str(e))
        return False


# ============================================
# 테스트 2: 기본 GET 조회
# ============================================

def test_basic_get_apis():
    """모든 테이블의 기본 GET 조회 테스트"""
    print_header('기본 GET API 테스트')
    
    # 각 테이블별 조회 테스트
    endpoints = [
        ('/customers', 'Customer 전체 조회'),
        ('/customers/1', 'Customer ID 조회'),
        ('/employees', 'Employee 전체 조회'),
        ('/employees/1', 'Employee ID 조회'),
        ('/manufacturers', 'Manufacturer 전체 조회'),
        ('/manufacturers/1', 'Manufacturer ID 조회'),
        ('/product_bases', 'ProductBase 전체 조회'),
        ('/product_bases/1', 'ProductBase ID 조회'),
        ('/product_images', 'ProductImage 전체 조회'),
        ('/product_images/1', 'ProductImage ID 조회'),
        ('/products', 'Product 전체 조회'),
        ('/products/1', 'Product ID 조회'),
        ('/purchases', 'Purchase 전체 조회'),
        ('/purchases/1', 'Purchase ID 조회'),
        ('/purchase_items', 'PurchaseItem 전체 조회'),
        ('/purchase_items/1', 'PurchaseItem ID 조회'),
        ('/login_histories', 'LoginHistory 전체 조회'),
        ('/login_histories/1', 'LoginHistory ID 조회'),
    ]
    
    for endpoint, name in endpoints:
        try:
            result = api_get(endpoint)
            # 결과가 있으면 성공
            success = 'results' in result or 'result' in result
            print_test(name, success)
        except Exception as e:
            print_test(name, False, str(e))


# ============================================
# 테스트 3: JOIN 쿼리 테스트
# ============================================

def test_join_apis():
    """
    복합 쿼리 (JOIN) API 테스트
    
    🚀 최적화 API 포함:
    
    1. /product_bases/list/full_detail
       - 기존: ProductBase + Product×N + Manufacturer×N (25회)
       - 개선: 1회 호출로 통합 조회
       - 응답: ProductBase + 첫이미지 + 대표Product + Manufacturer
    
    2. /purchases/list/with_items
       - 기존: Purchase + PurchaseItem×N (6회)
       - 개선: 1회 호출로 통합 조회
       - 응답: Purchase목록 + 각 주문별 PurchaseItem 배열
    
    3. /purchases/list/with_customer (cid 없이)
       - 기존: Purchase전체 + Customer×N (11회)
       - 개선: 1회 호출로 통합 조회
       - 응답: 전체 Purchase + Customer 정보 포함
    """
    print_header('JOIN API 테스트')
    
    join_endpoints = [
        # ─────────────────────────────────────────────────────────────
        # ProductBase 관련 JOIN
        # ─────────────────────────────────────────────────────────────
        ('/product_bases/1/with_images', 'ProductBase + 이미지 목록'),
        ('/product_bases/list/with_first_image', 'ProductBase 목록 + 첫번째 이미지'),
        
        # 🚀 최적화 API #1: 검색 화면용 (N번 호출 → 1번)
        # ProductBase + 첫이미지 + 대표Product + Manufacturer 통합
        ('/product_bases/list/full_detail', '🚀 ProductBase 전체 상세 (이미지+제품+제조사)'),
        
        # ─────────────────────────────────────────────────────────────
        # Product 관련 JOIN
        # ─────────────────────────────────────────────────────────────
        ('/products/1/with_base', 'Product + ProductBase'),
        ('/products/1/with_base_and_manufacturer', 'Product + ProductBase + Manufacturer'),
        ('/products/list/with_base?pbid=1', 'Product 목록 + ProductBase'),
        
        # ─────────────────────────────────────────────────────────────
        # Purchase 관련 JOIN
        # ─────────────────────────────────────────────────────────────
        ('/purchases/1/with_customer', 'Purchase + Customer'),
        ('/purchases/list/with_customer?cid=1', 'Purchase 목록 + Customer (cid 지정)'),
        
        # 🚀 최적화 API #2: 관리자 주문 화면용 (N번 호출 → 1번)
        # 전체 Purchase + Customer 통합
        ('/purchases/list/with_customer', '🚀 Purchase 전체 목록 + Customer (관리자용)'),
        
        # 🚀 최적화 API #3: 주문 목록 화면용 (N번 호출 → 1번)
        # Purchase + PurchaseItem 배열 통합
        ('/purchases/list/with_items?cid=1', '🚀 Purchase 목록 + 주문항목 (고객별)'),
        ('/purchases/list/with_items', '🚀 Purchase 전체 목록 + 주문항목'),
        
        # ─────────────────────────────────────────────────────────────
        # PurchaseItem 관련 JOIN (4테이블 조인)
        # ─────────────────────────────────────────────────────────────
        ('/purchase_items/1/with_product', 'PurchaseItem + Product'),
        ('/purchase_items/list/with_product?pcid=1', 'PurchaseItem 목록 + Product'),
        ('/purchase_items/1/full_detail', 'PurchaseItem 전체 상세 (4테이블 JOIN)'),
        ('/purchase_items/list/full_detail?pcid=1', 'PurchaseItem 목록 전체 상세'),
    ]
    
    for endpoint, name in join_endpoints:
        try:
            result = api_get(endpoint)
            success = 'results' in result or 'result' in result
            print_test(name, success)
        except Exception as e:
            print_test(name, False, str(e))


# ============================================
# 테스트 4: 필터링 및 부분 업데이트 API
# ============================================

def test_filter_and_patch_apis():
    """필터링 및 부분 업데이트 API 테스트 (Flutter 핸들러 호환용)"""
    print_header('필터링 및 부분 업데이트 API 테스트')
    
    # ---- Employee 필터 테스트 ----
    print('\n   --- Employee 필터 테스트 ---')
    
    # 1. Employee 생성 (테스트용)
    try:
        emp_data = {
            'eEmail': 'filtertest@store.com',
            'ePhoneNumber': '02-9999-8888',
            'eName': '필터테스트직원',
            'ePassword': 'pass123',
            'eRole': '1'
        }
        result = api_post('/employees', emp_data)
        emp_id = result.get('id')
        success = result.get('result') == 'OK'
        print_test('Employee 생성 (테스트용)', success, f"ID: {emp_id}")
    except Exception as e:
        print_test('Employee 생성 (테스트용)', False, str(e))
        emp_id = None
    
    # 2. 이메일로 Employee 필터 조회
    try:
        result = api_get('/employees?email=filtertest@store.com')
        employees = result.get('results', [])
        success = len(employees) > 0 and employees[0].get('eEmail') == 'filtertest@store.com'
        print_test('Employee 이메일 필터', success, f"조회: {len(employees)}건")
    except Exception as e:
        print_test('Employee 이메일 필터', False, str(e))
    
    # 3. 전화번호로 Employee 필터 조회
    try:
        result = api_get('/employees?phone=02-9999-8888')
        employees = result.get('results', [])
        success = len(employees) > 0
        print_test('Employee 전화번호 필터', success, f"조회: {len(employees)}건")
    except Exception as e:
        print_test('Employee 전화번호 필터', False, str(e))
    
    # 4. identifier로 Employee 필터 조회 (OR 조건)
    try:
        result = api_get('/employees?identifier=filtertest@store.com')
        employees = result.get('results', [])
        success = len(employees) > 0
        print_test('Employee identifier 필터 (OR)', success, f"조회: {len(employees)}건")
    except Exception as e:
        print_test('Employee identifier 필터 (OR)', False, str(e))
    
    # 5. 역할로 Employee 필터 조회
    try:
        result = api_get('/employees?role=1')
        employees = result.get('results', [])
        success = len(employees) > 0
        print_test('Employee 역할 필터', success, f"조회: {len(employees)}건")
    except Exception as e:
        print_test('Employee 역할 필터', False, str(e))
    
    # ---- Customer 필터 테스트 ----
    print('\n   --- Customer 필터 테스트 ---')
    
    # Customer 이메일 필터 (기존 데이터 사용)
    try:
        result = api_get('/customers?identifier=test')  # 이메일 또는 전화번호에 test 포함
        success = 'results' in result
        print_test('Customer identifier 필터', success)
    except Exception as e:
        print_test('Customer identifier 필터', False, str(e))
    
    # ---- LoginHistory 부분 업데이트 테스트 ----
    print('\n   --- LoginHistory 부분 업데이트 테스트 ---')
    
    # 1. Customer 생성 (테스트용)
    try:
        cust_data = {
            'cEmail': 'patchtest@test.com',
            'cPhoneNumber': '010-7777-8888',
            'cName': '패치테스트',
            'cPassword': 'pass123'
        }
        result = api_post('/customers', cust_data)
        cust_id = result.get('id')
        success = result.get('result') == 'OK'
        print_test('Customer 생성 (테스트용)', success, f"ID: {cust_id}")
    except Exception as e:
        print_test('Customer 생성 (테스트용)', False, str(e))
        cust_id = None
    
    # 2. LoginHistory 생성
    login_id = None
    if cust_id:
        try:
            login_data = {
                'cid': cust_id,
                'loginTime': '2025-12-25 10:00',
                'lStatus': 'active',
                'lVersion': 1.0,
                'lAddress': '테스트주소',
                'lPaymentMethod': 'Card'
            }
            result = api_post('/login_histories', login_data)
            login_id = result.get('id')
            success = result.get('result') == 'OK'
            print_test('LoginHistory 생성', success, f"ID: {login_id}")
        except Exception as e:
            print_test('LoginHistory 생성', False, str(e))
    
    # 3. PATCH - 상태 업데이트 (by_customer)
    if cust_id:
        try:
            result = api_patch(f'/login_histories/by_customer/{cust_id}/status?status=logged_out')
            success = result.get('result') == 'OK'
            affected = result.get('affected_rows', 0)
            print_test('LoginHistory 상태 PATCH', success, f"영향받은 행: {affected}")
        except Exception as e:
            print_test('LoginHistory 상태 PATCH', False, str(e))
    
    # 4. PATCH - 로그인 시간 업데이트 (by_customer)
    if cust_id:
        try:
            result = api_patch(f'/login_histories/by_customer/{cust_id}/login_time?login_time=2025-12-25 15:00')
            success = result.get('result') == 'OK'
            affected = result.get('affected_rows', 0)
            print_test('LoginHistory 시간 PATCH', success, f"영향받은 행: {affected}")
        except Exception as e:
            print_test('LoginHistory 시간 PATCH', False, str(e))
    
    # 5. 업데이트 확인
    if login_id:
        try:
            result = api_get(f'/login_histories/{login_id}')
            login = result.get('result', {})
            success = login.get('lStatus') == 'logged_out'
            print_test('PATCH 결과 확인', success, f"상태: {login.get('lStatus')}")
        except Exception as e:
            print_test('PATCH 결과 확인', False, str(e))
    
    # ---- 정리: 테스트 데이터 삭제 ----
    print('\n   --- 테스트 데이터 정리 ---')
    
    if login_id:
        try:
            result = api_delete(f'/login_histories/{login_id}')
            print_test('LoginHistory 삭제', result.get('result') == 'OK')
        except Exception as e:
            print_test('LoginHistory 삭제', False, str(e))
    
    if cust_id:
        try:
            result = api_delete(f'/customers/{cust_id}')
            print_test('Customer 삭제', result.get('result') == 'OK')
        except Exception as e:
            print_test('Customer 삭제', False, str(e))
    
    if emp_id:
        try:
            result = api_delete(f'/employees/{emp_id}')
            print_test('Employee 삭제', result.get('result') == 'OK')
        except Exception as e:
            print_test('Employee 삭제', False, str(e))


# ============================================
# 테스트 5: 회원가입 및 로그인
# ============================================

def test_signup_and_login():
    """회원가입 및 로그인 테스트"""
    print_header('회원가입 및 로그인 테스트')
    
    # 1. 회원 가입 (Customer POST)
    new_customer = {
        'cEmail': 'testuser@test.com',
        'cPhoneNumber': '010-1111-2222',
        'cName': '테스트사용자',
        'cPassword': 'password123'
    }
    
    try:
        result = api_post('/customers', new_customer)
        customer_id = result.get('id')
        success = result.get('result') == 'OK' and customer_id is not None
        print_test('회원 가입 (POST)', success, f"ID: {customer_id}")
    except Exception as e:
        print_test('회원 가입 (POST)', False, str(e))
        return None
    
    # 2. 로그인 이력 생성 (LoginHistory POST)
    login_data = {
        'cid': customer_id,
        'loginTime': '2025-12-25 12:00',
        'lStatus': '0',  # 로그인 상태
        'lVersion': 1.0,
        'lAddress': '테스트주소',
        'lPaymentMethod': 'CreditCard'
    }
    
    try:
        result = api_post('/login_histories', login_data)
        login_id = result.get('id')
        success = result.get('result') == 'OK' and login_id is not None
        print_test('로그인 이력 생성 (POST)', success, f"ID: {login_id}")
    except Exception as e:
        print_test('로그인 이력 생성 (POST)', False, str(e))
    
    # 3. 고객 정보 수정 (Customer PUT)
    update_customer = {
        'cEmail': 'updated@test.com',
        'cPhoneNumber': '010-3333-4444',
        'cName': '수정된사용자',
        'cPassword': 'newpassword'
    }
    
    try:
        result = api_put(f'/customers/{customer_id}', update_customer)
        success = result.get('result') == 'OK'
        print_test('고객 정보 수정 (PUT)', success)
    except Exception as e:
        print_test('고객 정보 수정 (PUT)', False, str(e))
    
    # 4. 수정된 정보 확인
    try:
        result = api_get(f'/customers/{customer_id}')
        customer = result.get('result', {})
        success = customer.get('cName') == '수정된사용자'
        print_test('수정된 정보 확인', success, f"이름: {customer.get('cName')}")
    except Exception as e:
        print_test('수정된 정보 확인', False, str(e))
    
    return customer_id


# ============================================
# 테스트 6: 주문 및 반품
# ============================================

def test_order_and_refund(customer_id: int):
    """주문 생성 및 반품 처리 테스트"""
    print_header('주문 및 반품 테스트')
    
    if customer_id is None:
        print('   ⚠️ 고객 ID가 없어 테스트를 건너뜁니다.')
        return
    
    # 1. 주문 생성 (Purchase POST)
    new_purchase = {
        'cid': customer_id,
        'pickupDate': '2025-12-30 14:00',
        'orderCode': 'TEST-ORDER-001',
        'timeStamp': '2025-12-25 12:30'
    }
    
    try:
        result = api_post('/purchases', new_purchase)
        purchase_id = result.get('id')
        success = result.get('result') == 'OK' and purchase_id is not None
        print_test('주문 생성 (POST)', success, f"주문 ID: {purchase_id}")
    except Exception as e:
        print_test('주문 생성 (POST)', False, str(e))
        return
    
    # 2. 주문 항목 추가 (PurchaseItem POST)
    items_to_add = [
        {'pid': 1, 'pcid': purchase_id, 'pcQuantity': 2, 'pcStatus': '제품 준비 중'},
        {'pid': 2, 'pcid': purchase_id, 'pcQuantity': 1, 'pcStatus': '제품 준비 중'}
    ]
    
    item_ids = []
    for i, item in enumerate(items_to_add, 1):
        try:
            result = api_post('/purchase_items', item)
            item_id = result.get('id')
            success = result.get('result') == 'OK' and item_id is not None
            print_test(f'주문 항목 {i} 추가 (POST)', success, f"항목 ID: {item_id}")
            if item_id:
                item_ids.append(item_id)
        except Exception as e:
            print_test(f'주문 항목 {i} 추가 (POST)', False, str(e))
    
    # ─────────────────────────────────────────────────────────────
    # 주문 상태 흐름 테스트 (config.dart + order_status_utils.dart 기준)
    # 
    # 상태 코드:
    #   0: 제품 준비 중
    #   1: 제품 준비 완료
    #   2: 제품 수령 완료
    #   3: 반품 신청
    #   4: 반품 처리 중
    #   5: 반품 완료
    #
    # 정상 흐름: 0 → 1 → 2
    # 반품 흐름: 2 → 3 → 4 → 5
    #
    # 비즈니스 규칙:
    #   - 반품 가능 조건: (상태 == 2) AND (픽업일로부터 30일 미경과)
    #   - 30일 경과 시: 자동으로 상태 2(제품 수령 완료)로 변경
    #   - 상태 0, 1에서는 반품 불가 (수령 전)
    #   - 상태 5(반품 완료)는 최종 상태
    # ─────────────────────────────────────────────────────────────
    
    # 3. 상태 변경: 제품 준비 중(0) → 제품 준비 완료(1)
    if item_ids:
        try:
            update_data = {
                'pid': 1,
                'pcid': purchase_id,
                'pcQuantity': 2,
                'pcStatus': '제품 준비 완료'  # 상태 1
            }
            result = api_put(f'/purchase_items/{item_ids[0]}', update_data)
            success = result.get('result') == 'OK'
            print_test('상태(0→1): 제품 준비 중 → 제품 준비 완료', success)
        except Exception as e:
            print_test('상태(0→1): 제품 준비 중 → 제품 준비 완료', False, str(e))
    
    # 4. 상태 변경: 제품 준비 완료(1) → 제품 수령 완료(2)
    if item_ids:
        try:
            pickup_data = {
                'pid': 1,
                'pcid': purchase_id,
                'pcQuantity': 2,
                'pcStatus': '제품 수령 완료'  # 상태 2
            }
            result = api_put(f'/purchase_items/{item_ids[0]}', pickup_data)
            success = result.get('result') == 'OK'
            print_test('상태(1→2): 제품 준비 완료 → 제품 수령 완료', success)
        except Exception as e:
            print_test('상태(1→2): 제품 준비 완료 → 제품 수령 완료', False, str(e))
    
    # 5. 상태 변경: 제품 수령 완료(2) → 반품 신청(3)
    # ※ 반품은 제품 수령 완료(2) 후에만 가능
    if item_ids:
        try:
            refund_data = {
                'pid': 1,
                'pcid': purchase_id,
                'pcQuantity': 2,
                'pcStatus': '반품 신청'  # 상태 3
            }
            result = api_put(f'/purchase_items/{item_ids[0]}', refund_data)
            success = result.get('result') == 'OK'
            print_test('상태(2→3): 제품 수령 완료 → 반품 신청', success)
        except Exception as e:
            print_test('상태(2→3): 제품 수령 완료 → 반품 신청', False, str(e))
    
    # 6. 상태 변경: 반품 신청(3) → 반품 처리 중(4)
    if item_ids:
        try:
            refund_data = {
                'pid': 1,
                'pcid': purchase_id,
                'pcQuantity': 2,
                'pcStatus': '반품 처리 중'  # 상태 4
            }
            result = api_put(f'/purchase_items/{item_ids[0]}', refund_data)
            success = result.get('result') == 'OK'
            print_test('상태(3→4): 반품 신청 → 반품 처리 중', success)
        except Exception as e:
            print_test('상태(3→4): 반품 신청 → 반품 처리 중', False, str(e))
    
    # 7. 상태 변경: 반품 처리 중(4) → 반품 완료(5)
    if item_ids:
        try:
            refund_data = {
                'pid': 1,
                'pcid': purchase_id,
                'pcQuantity': 2,
                'pcStatus': '반품 완료'  # 상태 5
            }
            result = api_put(f'/purchase_items/{item_ids[0]}', refund_data)
            success = result.get('result') == 'OK'
            print_test('상태(4→5): 반품 처리 중 → 반품 완료', success)
        except Exception as e:
            print_test('상태(4→5): 반품 처리 중 → 반품 완료', False, str(e))
    
    # 8. 두번째 항목: 정상 흐름 (제품 수령 완료)
    if len(item_ids) > 1:
        try:
            pickup_data = {
                'pid': 2,
                'pcid': purchase_id,
                'pcQuantity': 1,
                'pcStatus': '제품 수령 완료'  # 상태 2
            }
            result = api_put(f'/purchase_items/{item_ids[1]}', pickup_data)
            success = result.get('result') == 'OK'
            print_test('두번째 항목: 제품 수령 완료(2)', success)
        except Exception as e:
            print_test('두번째 항목: 제품 수령 완료(2)', False, str(e))
    
    # 9. 최종 상태 확인
    try:
        result = api_get(f'/purchase_items/list/full_detail?pcid={purchase_id}')
        items = result.get('results', [])
        success = len(items) == 2
        if success:
            for item in items:
                print(f'      - {item["pName"]} (사이즈: {item["size"]}) - {item["pcStatus"]}')
        print_test('최종 상태 확인', success, f"{len(items)}개 항목")
    except Exception as e:
        print_test('최종 상태 확인', False, str(e))


# ============================================
# 테스트 7: CRUD 전체 테스트 (생성 → 수정 → 삭제)
# ============================================

def test_full_crud():
    """생성, 수정, 삭제 전체 사이클 테스트"""
    print_header('CRUD 전체 사이클 테스트')
    
    created_ids = {}
    
    # 1. 제조사 생성
    try:
        result = api_post('/manufacturers', {'mName': 'TestBrand'})
        created_ids['manufacturer'] = result.get('id')
        success = result.get('result') == 'OK'
        print_test('Manufacturer 생성', success, f"ID: {created_ids.get('manufacturer')}")
    except Exception as e:
        print_test('Manufacturer 생성', False, str(e))
    
    # 2. ProductBase 생성
    try:
        pb_data = {
            'pName': '테스트제품',
            'pDescription': '테스트용 제품입니다',
            'pColor': 'Red',
            'pGender': 'Unisex',
            'pStatus': '',
            'pCategory': 'Test',
            'pModelNumber': 'TEST-001'
        }
        result = api_post('/product_bases', pb_data)
        created_ids['product_base'] = result.get('id')
        success = result.get('result') == 'OK'
        print_test('ProductBase 생성', success, f"ID: {created_ids.get('product_base')}")
    except Exception as e:
        print_test('ProductBase 생성', False, str(e))
    
    # 3. Product 생성
    if created_ids.get('manufacturer') and created_ids.get('product_base'):
        try:
            prod_data = {
                'pbid': created_ids['product_base'],
                'mfid': created_ids['manufacturer'],
                'size': 265,
                'basePrice': 99000,
                'pQuantity': 10
            }
            result = api_post('/products', prod_data)
            created_ids['product'] = result.get('id')
            success = result.get('result') == 'OK'
            print_test('Product 생성', success, f"ID: {created_ids.get('product')}")
        except Exception as e:
            print_test('Product 생성', False, str(e))
    
    # 4. ProductImage 생성
    if created_ids.get('product_base'):
        try:
            img_data = {
                'pbid': created_ids['product_base'],
                'imagePath': 'images/test/test_image.png'
            }
            result = api_post('/product_images', img_data)
            created_ids['product_image'] = result.get('id')
            success = result.get('result') == 'OK'
            print_test('ProductImage 생성', success, f"ID: {created_ids.get('product_image')}")
        except Exception as e:
            print_test('ProductImage 생성', False, str(e))
    
    # 5. 직원 생성
    try:
        emp_data = {
            'eEmail': 'teststaff@store.com',
            'ePhoneNumber': '02-0000-0000',
            'eName': '테스트직원',
            'ePassword': 'staffpass',
            'eRole': '1'
        }
        result = api_post('/employees', emp_data)
        created_ids['employee'] = result.get('id')
        success = result.get('result') == 'OK'
        print_test('Employee 생성', success, f"ID: {created_ids.get('employee')}")
    except Exception as e:
        print_test('Employee 생성', False, str(e))
    
    # 6. 직원 수정
    if created_ids.get('employee'):
        try:
            update_emp = {
                'eEmail': 'updated@store.com',
                'ePhoneNumber': '02-1111-1111',
                'eName': '수정된직원',
                'ePassword': 'newpass',
                'eRole': '2'
            }
            result = api_put(f'/employees/{created_ids["employee"]}', update_emp)
            success = result.get('result') == 'OK'
            print_test('Employee 수정', success)
        except Exception as e:
            print_test('Employee 수정', False, str(e))
    
    # 7. 삭제 테스트 (역순으로 진행)
    print('\n   --- 삭제 테스트 ---')
    
    # ProductImage 삭제
    if created_ids.get('product_image'):
        try:
            result = api_delete(f'/product_images/{created_ids["product_image"]}')
            success = result.get('result') == 'OK'
            print_test('ProductImage 삭제', success)
        except Exception as e:
            print_test('ProductImage 삭제', False, str(e))
    
    # Product 삭제
    if created_ids.get('product'):
        try:
            result = api_delete(f'/products/{created_ids["product"]}')
            success = result.get('result') == 'OK'
            print_test('Product 삭제', success)
        except Exception as e:
            print_test('Product 삭제', False, str(e))
    
    # ProductBase 삭제
    if created_ids.get('product_base'):
        try:
            result = api_delete(f'/product_bases/{created_ids["product_base"]}')
            success = result.get('result') == 'OK'
            print_test('ProductBase 삭제', success)
        except Exception as e:
            print_test('ProductBase 삭제', False, str(e))
    
    # Manufacturer 삭제
    if created_ids.get('manufacturer'):
        try:
            result = api_delete(f'/manufacturers/{created_ids["manufacturer"]}')
            success = result.get('result') == 'OK'
            print_test('Manufacturer 삭제', success)
        except Exception as e:
            print_test('Manufacturer 삭제', False, str(e))
    
    # Employee 삭제
    if created_ids.get('employee'):
        try:
            result = api_delete(f'/employees/{created_ids["employee"]}')
            success = result.get('result') == 'OK'
            print_test('Employee 삭제', success)
        except Exception as e:
            print_test('Employee 삭제', False, str(e))
    
    # 8. 삭제 확인
    if created_ids.get('product'):
        try:
            result = api_get(f'/products/{created_ids["product"]}')
            # 삭제되었으면 'not found' 메시지가 있어야 함
            success = 'not found' in result.get('message', '').lower()
            print_test('삭제 확인 (Product)', success)
        except Exception as e:
            print_test('삭제 확인 (Product)', False, str(e))


# ============================================
# 테스트 결과 출력
# ============================================

def print_summary():
    """테스트 결과 요약 출력"""
    print('\n' + '=' * 60)
    print('📊 테스트 결과 요약')
    print('=' * 60)
    
    total = test_results['passed'] + test_results['failed']
    pass_rate = (test_results['passed'] / total * 100) if total > 0 else 0
    
    print(f'\n   전체 테스트: {total}개')
    print(f'   ✅ 성공: {test_results["passed"]}개')
    print(f'   ❌ 실패: {test_results["failed"]}개')
    print(f'   📈 성공률: {pass_rate:.1f}%')
    
    # 실패한 테스트 목록
    failed_tests = [t for t in test_results['tests'] if not t['success']]
    if failed_tests:
        print('\n   --- 실패한 테스트 ---')
        for test in failed_tests:
            print(f'   ❌ {test["name"]}')
            if test['detail']:
                print(f'      원인: {test["detail"]}')
    
    print('\n' + '=' * 60)
    
    if test_results['failed'] == 0:
        print('🎉 모든 테스트가 성공했습니다!')
    else:
        print(f'⚠️ {test_results["failed"]}개의 테스트가 실패했습니다.')
    
    print('=' * 60)


# ============================================
# 메인 실행
# ============================================

def main():
    """메인 테스트 실행 함수"""
    print('\n' + '🚀' * 20)
    print('\n   FastAPI 백엔드 API 테스트')
    print(f'   서버: {BASE_URL}')
    print('\n' + '🚀' * 20)
    
    # 1. 헬스 체크
    if not test_health_check():
        print('\n⚠️ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.')
        print('   uvicorn app.main:app --host 127.0.0.1 --port 8000')
        return
    
    # 2. 기본 GET API 테스트
    test_basic_get_apis()
    
    # 3. JOIN API 테스트 (새로 추가된 API 포함)
    test_join_apis()
    
    # 4. 필터링 및 부분 업데이트 API 테스트 (Flutter 핸들러 호환용)
    test_filter_and_patch_apis()
    
    # 5. 회원가입 및 로그인 테스트
    customer_id = test_signup_and_login()
    
    # 6. 주문 및 반품 테스트
    test_order_and_refund(customer_id)
    
    # 7. CRUD 전체 테스트
    test_full_crud()
    
    # 결과 요약 출력
    print_summary()


if __name__ == '__main__':
    main()

