# API 테스트 결과 문서

> 테스트 일자: 2025-12-25 (업데이트)
> 테스트 환경: FastAPI + MySQL (외부 서버)
> 서버 주소: http://127.0.0.1:8000

---

## 📊 전체 테스트 요약

| 상태 | 개수 | 비율 |
|------|------|------|
| ✅ 성공 | 72개 | 100% |
| ❌ 실패 | 0개 | 0% |

---

## 1. 기본 CRUD API 테스트 (GET)

### 헬스 체크
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/health` | 서버 상태 + DB 연결 확인 | ✅ 성공 |

### Customer (고객)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/customers` | 전체 고객 조회 | ✅ 성공 |
| 2 | GET `/api/customers/{id}` | ID로 고객 조회 | ✅ 성공 |
| 3 | GET `/api/customers?email=...` | 이메일 필터 | ✅ 성공 |
| 4 | GET `/api/customers?phone=...` | 전화번호 필터 | ✅ 성공 |
| 5 | GET `/api/customers?identifier=...` | 이메일 또는 전화번호 필터 (OR) | ✅ 성공 |

### Employee (직원)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/employees` | 전체 직원 조회 | ✅ 성공 |
| 2 | GET `/api/employees/{id}` | ID로 직원 조회 | ✅ 성공 |
| 3 | GET `/api/employees?email=...` | 이메일 필터 | ✅ 성공 |
| 4 | GET `/api/employees?phone=...` | 전화번호 필터 | ✅ 성공 |
| 5 | GET `/api/employees?identifier=...` | 이메일 또는 전화번호 필터 (OR) | ✅ 성공 |
| 6 | GET `/api/employees?role=...` | 역할 필터 | ✅ 성공 |

### Manufacturer (제조사)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/manufacturers` | 전체 제조사 조회 | ✅ 성공 |
| 2 | GET `/api/manufacturers/{id}` | ID로 제조사 조회 | ✅ 성공 |

### ProductBase (제품 기본 정보)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/product_bases` | 전체 ProductBase 조회 | ✅ 성공 |
| 2 | GET `/api/product_bases/{id}` | ID로 ProductBase 조회 | ✅ 성공 |
| 3 | GET `/api/product_bases/{id}/with_images` | +이미지 JOIN | ✅ 성공 |
| 4 | GET `/api/product_bases/list/with_first_image` | +첫번째 이미지 JOIN | ✅ 성공 |
| 5 | GET `/api/product_bases/list/full_detail` | **전체 상세 (이미지+제품+제조사)** | ✅ 성공 |

### ProductImage (제품 이미지)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/product_images` | 전체 이미지 조회 | ✅ 성공 |
| 2 | GET `/api/product_images/{id}` | ID로 이미지 조회 | ✅ 성공 |

### Product (제품)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/products` | 전체 제품 조회 | ✅ 성공 |
| 2 | GET `/api/products/{id}` | ID로 제품 조회 | ✅ 성공 |
| 3 | GET `/api/products?pbid=1` | ProductBase 필터 | ✅ 성공 |
| 4 | GET `/api/products/{id}/with_base` | +ProductBase JOIN | ✅ 성공 |
| 5 | GET `/api/products/{id}/with_base_and_manufacturer` | +ProductBase+Manufacturer JOIN | ✅ 성공 |
| 6 | GET `/api/products/list/with_base?pbid=1` | 목록+ProductBase JOIN | ✅ 성공 |

### Purchase (주문)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/purchases` | 전체 주문 조회 | ✅ 성공 |
| 2 | GET `/api/purchases/{id}` | ID로 주문 조회 | ✅ 성공 |
| 3 | GET `/api/purchases?cid=1` | 고객별 필터 | ✅ 성공 |
| 4 | GET `/api/purchases/{id}/with_customer` | +고객 정보 JOIN | ✅ 성공 |
| 5 | GET `/api/purchases/list/with_customer?cid=1` | 목록+고객 정보 JOIN (고객별) | ✅ 성공 |
| 6 | GET `/api/purchases/list/with_customer` | **전체 목록+고객 정보 (관리자용)** | ✅ 성공 |
| 7 | GET `/api/purchases/list/with_items?cid=1` | **목록+주문항목 (고객별)** | ✅ 성공 |
| 8 | GET `/api/purchases/list/with_items` | **전체 목록+주문항목** | ✅ 성공 |

### PurchaseItem (주문 항목)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/purchase_items` | 전체 주문 항목 조회 | ✅ 성공 |
| 2 | GET `/api/purchase_items/{id}` | ID로 주문 항목 조회 | ✅ 성공 |
| 3 | GET `/api/purchase_items?pcid=1` | 주문별 필터 | ✅ 성공 |
| 4 | GET `/api/purchase_items/{id}/with_product` | +제품 정보 JOIN | ✅ 성공 |
| 5 | GET `/api/purchase_items/list/with_product?pcid=1` | 목록+제품 정보 JOIN | ✅ 성공 |
| 6 | GET `/api/purchase_items/{id}/full_detail` | 전체 상세 JOIN (4테이블) | ✅ 성공 |
| 7 | GET `/api/purchase_items/list/full_detail?pcid=1` | 목록 전체 상세 JOIN | ✅ 성공 |

### LoginHistory (로그인 이력)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/login_histories` | 전체 로그인 이력 조회 | ✅ 성공 |
| 2 | GET `/api/login_histories/{id}` | ID로 로그인 이력 조회 | ✅ 성공 |
| 3 | GET `/api/login_histories?cid=1` | 고객별 필터 | ✅ 성공 |
| 4 | PATCH `/api/login_histories/by_customer/{cid}/status` | **상태 부분 업데이트** | ✅ 성공 |
| 5 | PATCH `/api/login_histories/by_customer/{cid}/login_time` | **로그인 시간 부분 업데이트** | ✅ 성공 |

---

## 2. 회원가입, 로그인, 주문, 반품 테스트

| # | 테스트 항목 | API | 결과 |
|---|------------|-----|------|
| 1 | 회원 가입 | POST `/customers` | ✅ 성공 |
| 2 | 로그인 이력 생성 | POST `/login_histories` | ✅ 성공 |
| 3 | 주문 생성 | POST `/purchases` | ✅ 성공 |
| 4 | 주문 항목 추가 | POST `/purchase_items` | ✅ 성공 (2개 항목) |
| 5 | 주문 + 고객 조회 | GET `/purchases/{id}/with_customer` | ✅ 성공 |
| 6 | 주문 항목 상세 조회 | GET `/purchase_items/list/full_detail` | ✅ 성공 |
| 7 | 주문 상태 변경 (준비 완료) | PUT `/purchase_items/{id}` | ✅ 성공 |
| 8 | **반품 처리** | PUT `/purchase_items/{id}` (→ 반품) | ✅ 성공 |
| 9 | 최종 상태 확인 | GET `/purchase_items/list/full_detail` | ✅ 성공 |
| 10 | 고객 정보 수정 | PUT `/customers/{id}` | ✅ 성공 |
| 11 | 수정된 고객 확인 | GET `/customers/{id}` | ✅ 성공 |

---

## 3. CRUD 전체 기능 테스트

| # | 테스트 항목 | API | 결과 |
|---|------------|-----|------|
| 1 | 제품 수령 완료 | PUT `/purchase_items/{id}` (→ 수령 완료) | ✅ 성공 |
| 2 | 직원 생성 | POST `/employees` | ✅ 성공 |
| 3 | 직원 수정 | PUT `/employees/{id}` | ✅ 성공 |
| 4 | 제조사 생성 | POST `/manufacturers` | ✅ 성공 |
| 5 | ProductBase 생성 | POST `/product_bases` | ✅ 성공 |
| 6 | Product 생성 | POST `/products` | ✅ 성공 |
| 7 | ProductImage 생성 | POST `/product_images` | ✅ 성공 |
| 8 | Product 상세 조회 | GET `/products/{id}/with_base_and_manufacturer` | ✅ 성공 |
| 9 | ProductImage 삭제 | DELETE `/product_images/{id}` | ✅ 성공 |
| 10 | Product 삭제 | DELETE `/products/{id}` | ✅ 성공 |
| 11 | ProductBase 삭제 | DELETE `/product_bases/{id}` | ✅ 성공 |
| 12 | Manufacturer 삭제 | DELETE `/manufacturers/{id}` | ✅ 성공 |
| 13 | Employee 삭제 | DELETE `/employees/{id}` | ✅ 성공 |
| 14 | 삭제 확인 | GET `/products/{id}` → not found | ✅ 성공 |

---

## 4. CRUD 메서드 커버리지

| 기능 | GET | POST | PUT | PATCH | DELETE |
|------|-----|------|-----|-------|--------|
| Customer (고객) | ✅ | ✅ | ✅ | - | ✅ |
| Employee (직원) | ✅ | ✅ | ✅ | - | ✅ |
| Manufacturer (제조사) | ✅ | ✅ | - | - | ✅ |
| ProductBase | ✅ | ✅ | - | - | ✅ |
| ProductImage | ✅ | ✅ | - | - | ✅ |
| Product | ✅ | ✅ | - | - | ✅ |
| Purchase (주문) | ✅ | ✅ | ✅ | - | - |
| PurchaseItem (주문 항목) | ✅ | ✅ | ✅ | - | - |
| LoginHistory (로그인 이력) | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 5. 주문 상태 흐름 테스트

### 상태 코드 정의 (config.dart 기준)

| 코드 | 상태명 | 설명 |
|------|--------|------|
| 0 | 제품 준비 중 | 주문 접수 후 초기 상태 |
| 1 | 제품 준비 완료 | 직원이 제품 준비 완료 처리 |
| 2 | 제품 수령 완료 | 고객이 픽업 완료 |
| 3 | 반품 신청 | 고객이 반품 요청 |
| 4 | 반품 처리 중 | 직원이 반품 처리 중 |
| 5 | 반품 완료 | 반품 처리 완료 |

### 상태 흐름도

```
[정상 흐름]
제품 준비 중(0) → 제품 준비 완료(1) → 제품 수령 완료(2)

[반품 흐름] ※ 제품 수령 완료(2) 이후에만 가능
제품 수령 완료(2) → 반품 신청(3) → 반품 처리 중(4) → 반품 완료(5)
```

### 비즈니스 규칙 (order_status_utils.dart 기준)

#### 반품 가능 조건
```
반품 가능 = (상태 == 2 "제품 수령 완료") AND (픽업일로부터 30일 미경과)
```

| 조건 | 반품 가능 |
|------|----------|
| 상태 0, 1 (수령 전) | ❌ 불가 |
| 상태 2 + 30일 미경과 | ✅ 가능 |
| 상태 2 + 30일 경과 | ❌ 불가 (자동 완료) |
| 상태 3, 4 (반품 진행 중) | ❌ 불가 |
| 상태 5 (반품 완료) | ❌ 불가 |

#### 자동 상태 변경
- **30일 경과 시**: 상태 2 미만인 항목 → 자동으로 상태 2(제품 수령 완료)로 변경
- **날짜 기반 표시**: 구매 당일(0), 픽업일 도래(1), 30일 경과(2)

### 테스트 결과

| 상태 변경 | 테스트 결과 | 비고 |
|----------|------------|------|
| 제품 준비 중(0) → 제품 준비 완료(1) | ✅ 성공 | 직원이 제품 준비 완료 처리 |
| 제품 준비 완료(1) → 제품 수령 완료(2) | ✅ 성공 | 고객이 픽업 완료 |
| 제품 수령 완료(2) → 반품 신청(3) | ✅ 성공 | 수령 후 30일 내 반품 신청 |
| 반품 신청(3) → 반품 처리 중(4) | ✅ 성공 | 직원이 반품 접수 |
| 반품 처리 중(4) → 반품 완료(5) | ✅ 성공 | 반품 처리 완료 |

---

## 6. 추가된 API (Flutter 핸들러 호환용)

### 2025-12-25 추가

| # | 엔드포인트 | 설명 | 용도 |
|---|-----------|------|------|
| 1 | GET `/api/employees?email=...` | 이메일 필터 | 직원 로그인 |
| 2 | GET `/api/employees?phone=...` | 전화번호 필터 | 직원 검색 |
| 3 | GET `/api/employees?identifier=...` | 이메일/전화번호 OR 필터 | 통합 검색 |
| 4 | GET `/api/employees?role=...` | 역할 필터 | 역할별 조회 |
| 5 | PATCH `/login_histories/by_customer/{cid}/status` | 상태 부분 업데이트 | 로그인 상태 변경 |
| 6 | PATCH `/login_histories/by_customer/{cid}/login_time` | 시간 부분 업데이트 | 로그인 시간 갱신 |
| 7 | GET `/api/product_bases/list/full_detail` | 전체 상세 목록 | 검색 화면 |
| 8 | GET `/api/purchases/list/with_customer` | 전체 주문+고객 | 관리자 화면 |
| 9 | GET `/api/purchases/list/with_items` | 주문+항목 목록 | 주문 목록 화면 |

---

## 7. 수정된 버그

### 라우터 순서 문제 (수정 완료)

| 파일 | 문제 | 해결 |
|------|------|------|
| `products.py` | `/list/with_base`가 `/{id}`에 매칭됨 | 라우트 순서 변경 |
| `purchases.py` | `/list/with_customer`가 `/{id}`에 매칭됨 | 라우트 순서 변경 |
| `purchase_items.py` | `/list/*`가 `/{id}`에 매칭됨 | 라우트 순서 변경 |
| `product_bases.py` | `/list/with_first_image`가 `/{id}`에 매칭됨 + 컬럼 매핑 오류 | 라우트 순서 변경 + 명시적 컬럼 선택 |
| `login_histories.py` | `/by_customer/*`가 `/{id}`에 매칭됨 | 라우트 순서 변경 |

---

## 📋 HTTP 메서드 가이드

### 기본 개념

HTTP 메서드는 서버에 "어떤 작업을 할지" 알려주는 명령어입니다.

| HTTP 메서드 | SQL | CRUD | 한줄 설명 |
|------------|-----|------|----------|
| **GET** | SELECT | Read | 데이터 **조회** (가져오기) |
| **POST** | INSERT | Create | 데이터 **생성** (새로 만들기) |
| **PUT** | UPDATE | Update | 데이터 **전체 수정** (덮어쓰기) |
| **PATCH** | UPDATE | Update | 데이터 **부분 수정** (일부만 변경) |
| **DELETE** | DELETE | Delete | 데이터 **삭제** (지우기) |

---

### 🔑 PUT vs PATCH 차이점 (중요!)

둘 다 데이터를 수정하지만, **수정 범위**가 다릅니다.

#### PUT = 전체 교체 (Replace)

**모든 필드를 다 보내야 합니다.** 안 보낸 필드는 NULL이 됩니다.

```
PUT /api/customers/1

보내는 데이터:
{
  "cEmail": "new@test.com",      ← 변경할 값
  "cPhoneNumber": "010-1234-5678", ← 안 바꿔도 보내야 함
  "cName": "홍길동",               ← 안 바꿔도 보내야 함  
  "cPassword": "pass123"          ← 안 바꿔도 보내야 함
}
```

#### PATCH = 부분 수정 (Modify)

**변경할 필드만 보내면 됩니다.** 나머지는 기존 값 유지.

```
PATCH /api/login_histories/by_customer/1/status?status=logged_out

→ lStatus 필드만 "logged_out"으로 변경
→ 나머지 필드(loginTime, lVersion 등)는 그대로 유지
```

---

### 📌 언제 어떤 메서드를 사용하나?

| 상황 | 적합한 메서드 | 이유 |
|------|-------------|------|
| 고객 정보 수정 폼 (전체 입력) | **PUT** | 모든 필드를 한번에 저장 |
| 로그인 상태만 변경 | **PATCH** | 상태 필드 하나만 변경 |
| 비밀번호만 변경 | **PATCH** | 비밀번호 필드만 변경 |
| 주문 상태 업데이트 | **PUT** 또는 **PATCH** | 상황에 따라 선택 |
| 프로필 사진만 변경 | **PATCH** | 사진 필드만 변경 |

---

### 🌐 실제 요청 예시 (Flutter에서 사용 시)

#### GET - 데이터 조회
```dart
// 고객 목록 가져오기
final response = await http.get(Uri.parse('$baseUrl/api/customers'));
```

#### POST - 데이터 생성
```dart
// 새 고객 등록
final response = await http.post(
  Uri.parse('$baseUrl/api/customers'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'cEmail': 'user@test.com',
    'cPhoneNumber': '010-1234-5678',
    'cName': '홍길동',
    'cPassword': 'password123'
  }),
);
```

#### PUT - 전체 수정
```dart
// 고객 정보 전체 수정 (모든 필드 필요)
final response = await http.put(
  Uri.parse('$baseUrl/api/customers/1'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'cEmail': 'updated@test.com',
    'cPhoneNumber': '010-9999-8888',
    'cName': '김철수',
    'cPassword': 'newpassword'
  }),
);
```

#### PATCH - 부분 수정
```dart
// 로그인 상태만 변경 (한 필드만)
final response = await http.patch(
  Uri.parse('$baseUrl/api/login_histories/by_customer/1/status?status=logged_out'),
);
```

#### DELETE - 삭제
```dart
// 고객 삭제
final response = await http.delete(Uri.parse('$baseUrl/api/customers/1'));
```

---

### 📊 우리 프로젝트의 PATCH API 목록

| 엔드포인트 | 용도 | 변경되는 필드 |
|-----------|------|-------------|
| `PATCH /login_histories/by_customer/{cid}/status` | 로그인 상태 변경 | lStatus |
| `PATCH /login_histories/by_customer/{cid}/login_time` | 로그인 시간 갱신 | loginTime |

---

### 💡 팁: 메서드 선택 기준

```
데이터를 가져올 때 → GET
새 데이터를 만들 때 → POST
데이터 전체를 바꿀 때 → PUT
데이터 일부만 바꿀 때 → PATCH
데이터를 지울 때 → DELETE
```

---

## 🔄 Flutter SQLite 핸들러 → FastAPI 매핑

### 즉시 대체 가능 (21개)

| Flutter Handler Method | FastAPI Endpoint |
|-----------------------|------------------|
| `CustomerHandler.queryAll()` | `GET /api/customers` |
| `CustomerHandler.queryById(id)` | `GET /api/customers/{id}` |
| `CustomerHandler.queryByEmailOrPhone(identifier)` | `GET /api/customers?identifier=...` |
| `CustomerHandler.insertData(data)` | `POST /api/customers` |
| `CustomerHandler.updateData(data)` | `PUT /api/customers/{id}` |
| `EmployeeHandler.queryAll()` | `GET /api/employees` |
| `EmployeeHandler.queryById(id)` | `GET /api/employees/{id}` |
| `EmployeeHandler.queryByEmailOrPhone(identifier)` | `GET /api/employees?identifier=...` |
| `PurchaseHandler.queryAll()` | `GET /api/purchases` |
| `PurchaseHandler.queryById(id)` | `GET /api/purchases/{id}` |
| `PurchaseHandler.queryByCustomerId(cid)` | `GET /api/purchases?cid=...` |
| `PurchaseHandler.insertData(data)` | `POST /api/purchases` |
| `PurchaseItemHandler.queryByPurchaseId(pcid)` | `GET /api/purchase_items?pcid=...` |
| `PurchaseItemHandler.insertData(data)` | `POST /api/purchase_items` |
| `PurchaseItemHandler.updateData(data)` | `PUT /api/purchase_items/{id}` |
| `ProductBaseHandler.queryListWithFirstImage()` | `GET /api/product_bases/list/with_first_image` |
| `ProductHandler.queryWithBase(id)` | `GET /api/products/{id}/with_base` |
| `ProductHandler.queryByProductBaseId(pbid)` | `GET /api/products?pbid=...` |
| `LoginHistoryHandler.queryByCustomerId(cid)` | `GET /api/login_histories?cid=...` |
| `LoginHistoryHandler.insertData(data)` | `POST /api/login_histories` |
| `LoginHistoryHandler.updateData(data)` | `PUT /api/login_histories/{id}` |

### 최적화된 통합 API (순차 호출 대체)

| 기존 패턴 (N번 호출) | 새 API (1번 호출) |
|--------------------|------------------|
| ProductBase + Product + Manufacturer 루프 | `GET /api/product_bases/list/full_detail` |
| Purchase + PurchaseItem 루프 | `GET /api/purchases/list/with_items` |
| 전체 Purchase + Customer | `GET /api/purchases/list/with_customer` |

---

## 🚀 최적화 API 상세 설명

### 1. `GET /api/product_bases/list/full_detail`

**용도:** 검색/제품 목록 화면 (search_view.dart)

#### 기존 Flutter 패턴 (N번 호출)
```dart
// 1. ProductBase + 첫번째 이미지 조회
final productsWithImages = await _productBaseHandler.queryListWithFirstImage();

// 2. 각 ProductBase별 Product 조회 (N회 반복)
for (final pbid in pbids) {
  final products = await _productHandler.queryByProductBaseId(pbid);
  // ...
}

// 3. 각 Product별 Manufacturer 조회 (N회 반복)
for (final mfid in mfids) {
  final manufacturer = await _manufacturerHandler.queryById(mfid);
  // ...
}
```

#### 새 API (1번 호출)
```dart
final response = await http.get('/api/product_bases/list/full_detail');
```

#### 응답 형식
```json
{
  "results": [
    {
      "id": 1,
      "pName": "U740WN2",
      "pDescription": "뉴발란스 클래식",
      "pColor": "Black",
      "pGender": "Unisex",
      "pStatus": "",
      "pCategory": "Running",
      "pModelNumber": "U740WN2",
      "firstImage": "images/shoes/u740wn2_1.jpg",
      "representativeProduct": {
        "id": 1,
        "size": 260,
        "basePrice": 149000,
        "discountRate": 0,
        "stock": 10
      },
      "manufacturer": {
        "id": 2,
        "mName": "NewBalance",
        "mDescription": "뉴발란스 코리아"
      }
    }
  ]
}
```

#### 성능 개선
| 항목 | 기존 | 개선 | 감소율 |
|------|------|------|--------|
| 제품 12개 기준 | 1 + 12 + 12 = **25회** | **1회** | 96% ↓ |

---

### 2. `GET /api/purchases/list/with_items`

**용도:** 주문 목록 화면 (order_list_view.dart)

#### 기존 Flutter 패턴 (N번 호출)
```dart
// 1. 고객별 주문 목록 조회
final purchases = await _purchaseHandler.queryByCustomerId(userId);

// 2. 각 주문별 주문항목 조회 (N회 반복)
for (final purchase in purchases) {
  final items = await _purchaseItemHandler.queryByPurchaseId(purchase.id!);
  // 상태 계산 등...
}
```

#### 새 API (1번 호출)
```dart
// 특정 고객의 주문
final response = await http.get('/api/purchases/list/with_items?cid=1');

// 전체 주문 (관리자)
final response = await http.get('/api/purchases/list/with_items');
```

#### 응답 형식
```json
{
  "results": [
    {
      "id": 1,
      "cid": 1,
      "pickupDate": "2025-12-30 14:00",
      "orderCode": "ORDER-001",
      "timeStamp": "2025-12-25 12:30",
      "items": [
        {
          "id": 1,
          "pid": 1,
          "pcid": 1,
          "pcQuantity": 2,
          "pcStatus": "제품 준비 완료"
        },
        {
          "id": 2,
          "pid": 2,
          "pcid": 1,
          "pcQuantity": 1,
          "pcStatus": "제품 준비 중"
        }
      ],
      "itemCount": 2
    }
  ]
}
```

#### 성능 개선
| 항목 | 기존 | 개선 | 감소율 |
|------|------|------|--------|
| 주문 5개 기준 | 1 + 5 = **6회** | **1회** | 83% ↓ |

---

### 3. `GET /api/purchases/list/with_customer`

**용도:** 관리자 주문 관리 화면 (admin_order_view.dart)

#### 기존 Flutter 패턴 (N번 호출)
```dart
// 1. 전체 주문 조회
final purchases = await _purchaseHandler.queryAll();

// 2. 각 주문별 고객 정보 조회 (N회 반복)
for (final purchase in purchases) {
  final customer = await _customerHandler.queryById(purchase.cid!);
  // ...
}
```

#### 새 API (1번 호출)
```dart
// 전체 주문 + 고객 정보 (관리자용)
final response = await http.get('/api/purchases/list/with_customer');

// 특정 고객의 주문 + 고객 정보
final response = await http.get('/api/purchases/list/with_customer?cid=1');
```

#### 응답 형식
```json
{
  "results": [
    {
      "id": 1,
      "cid": 1,
      "pickupDate": "2025-12-30 14:00",
      "orderCode": "ORDER-001",
      "timeStamp": "2025-12-25 12:30",
      "cName": "홍길동",
      "cEmail": "hong@test.com",
      "cPhoneNumber": "010-1234-5678"
    }
  ]
}
```

#### 성능 개선
| 항목 | 기존 | 개선 | 감소율 |
|------|------|------|--------|
| 주문 10개 기준 | 1 + 10 = **11회** | **1회** | 91% ↓ |

---

## 📊 전체 성능 개선 요약

| 화면 | 기존 호출 | 개선 후 | 감소율 | 사용 API |
|------|----------|---------|--------|----------|
| 검색 화면 | 25회 | 1회 | **96%** | `/product_bases/list/full_detail` |
| 주문 목록 | 6회 | 1회 | **83%** | `/purchases/list/with_items` |
| 관리자 주문 | 11회 | 1회 | **91%** | `/purchases/list/with_customer` |

