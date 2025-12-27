# API 테스트 결과 문서

> 테스트 일자: 2025-12-27 (최신 업데이트)
> 테스트 환경: FastAPI + MySQL (외부 서버)
> 서버 주소: http://127.0.0.1:8000

---

## 📊 전체 테스트 요약

| 상태 | 개수 | 비율 |
|------|------|------|
| ✅ 성공 | 79개 | 100% |
| ❌ 실패 | 0개 | 0% |

**✅ 모든 테스트 통과!** 데이터베이스 초기화 후 모든 기능이 정상 작동합니다.

---

## 🆕 최신 변경 사항 (2025-12-27)

### Customer/Employee 프로필 이미지 기능 추가

| 기능 | 엔드포인트 | 설명 | 결과 |
|------|-----------|------|------|
| INSERT (이미지 포함 필수) | POST `/api/customers` | Form + UploadFile | ✅ 성공 |
| INSERT (이미지 포함 필수) | POST `/api/employees` | Form + UploadFile | ✅ 성공 |
| UPDATE (이미지 제외) | PUT `/api/customers/{id}` | JSON Body | ✅ 성공 |
| UPDATE (이미지 제외) | PUT `/api/employees/{id}` | JSON Body | ✅ 성공 |
| UPDATE (이미지 포함) | POST `/api/customers/{id}/with_image` | Form + UploadFile | ✅ 성공 |
| UPDATE (이미지 포함) | POST `/api/employees/{id}/with_image` | Form + UploadFile | ✅ 성공 |
| 프로필 이미지 조회 | GET `/api/customers/{id}/profile_image` | Response (바이너리) | ✅ 성공 |
| 프로필 이미지 조회 | GET `/api/employees/{id}/profile_image` | Response (바이너리) | ✅ 성공 |
| 프로필 이미지 삭제 | DELETE `/api/customers/{id}/profile_image` | NULL로 업데이트 | ✅ 성공 |
| 프로필 이미지 삭제 | DELETE `/api/employees/{id}/profile_image` | NULL로 업데이트 | ✅ 성공 |

### 주요 변경점

1. **INSERT**: 이미지 업로드 필수 (Form + UploadFile)
2. **UPDATE**: 두 가지 방식 제공
   - 이미지 제외: PUT `/api/{resource}/{id}` (JSON Body)
   - 이미지 포함: POST `/api/{resource}/{id}/with_image` (Form + UploadFile)
3. **이미지 조회**: Response 객체로 바이너리 직접 반환 (base64 인코딩 제거)
4. **이미지 삭제**: 별도 엔드포인트 제공

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
| 3 | GET `/api/customers/{id}/profile_image` | 프로필 이미지 조회 | ✅ 성공 |
| 4 | GET `/api/customers?identifier=...` | 이메일 또는 전화번호 필터 (OR) | ✅ 성공 |

### Employee (직원)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/employees` | 전체 직원 조회 | ✅ 성공 |
| 2 | GET `/api/employees/{id}` | ID로 직원 조회 | ✅ 성공 |
| 3 | GET `/api/employees/{id}/profile_image` | 프로필 이미지 조회 | ✅ 성공 |
| 4 | GET `/api/employees?role=...` | 역할 필터 | ✅ 성공 |

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
| 3 | GET `/api/products/{id}/with_base` | +ProductBase JOIN | ✅ 성공 |
| 4 | GET `/api/products/{id}/with_base_and_manufacturer` | +ProductBase+Manufacturer JOIN | ✅ 성공 |
| 5 | GET `/api/products/list/with_base?pbid=1` | 목록+ProductBase JOIN | ✅ 성공 |

### Purchase (주문)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/purchases` | 전체 주문 조회 | ✅ 성공 |
| 2 | GET `/api/purchases/{id}` | ID로 주문 조회 | ✅ 성공 |
| 3 | GET `/api/purchases/{id}/with_customer` | +고객 정보 JOIN | ✅ 성공 |
| 4 | GET `/api/purchases/list/with_customer` | **전체 목록+고객 정보 (관리자용)** | ✅ 성공 |
| 5 | GET `/api/purchases/list/with_items` | **전체 목록+주문항목** | ✅ 성공 |

### PurchaseItem (주문 항목)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/purchase_items` | 전체 주문 항목 조회 | ✅ 성공 |
| 2 | GET `/api/purchase_items/{id}` | ID로 주문 항목 조회 | ✅ 성공 |
| 3 | GET `/api/purchase_items/{id}/with_product` | +제품 정보 JOIN | ✅ 성공 |
| 4 | GET `/api/purchase_items/{id}/full_detail` | 전체 상세 JOIN (4테이블) | ✅ 성공 |
| 5 | GET `/api/purchase_items/list/full_detail?pcid=1` | 목록 전체 상세 JOIN | ✅ 성공 |

### LoginHistory (로그인 이력)
| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/api/login_histories` | 전체 로그인 이력 조회 | ✅ 성공 |
| 2 | GET `/api/login_histories/{id}` | ID로 로그인 이력 조회 | ✅ 성공 |
| 3 | PATCH `/api/login_histories/by_customer/{cid}/status` | **상태 부분 업데이트** | ✅ 성공 |
| 4 | PATCH `/api/login_histories/by_customer/{cid}/login_time` | **로그인 시간 부분 업데이트** | ✅ 성공 |

---

## 2. 회원가입, 로그인, 프로필 이미지 테스트

| # | 테스트 항목 | API | 결과 |
|---|------------|-----|------|
| 1 | 회원 가입 (이미지 포함) | POST `/customers` (Form + UploadFile) | ✅ 성공 |
| 2 | 로그인 이력 생성 | POST `/login_histories` | ✅ 성공 |
| 3 | 프로필 이미지 조회 | GET `/customers/{id}/profile_image` | ✅ 성공 |
| 4 | 고객 정보 수정 (이미지 포함) | POST `/customers/{id}/with_image` | ✅ 성공 |

---

## 3. CRUD 전체 기능 테스트

| # | 테스트 항목 | API | 결과 |
|---|------------|-----|------|
| 1 | Manufacturer 생성 | POST `/manufacturers` | ✅ 성공 |
| 2 | Employee 생성 (이미지 포함) | POST `/employees` (Form + UploadFile) | ✅ 성공 |
| 3 | Employee 수정 (이미지 제외) | PUT `/employees/{id}` | ✅ 성공 |
| 4 | Employee 프로필 이미지 조회 | GET `/employees/{id}/profile_image` | ✅ 성공 |
| 5 | Employee 정보 수정 (이미지 포함) | POST `/employees/{id}/with_image` | ✅ 성공 |
| 6 | Manufacturer 삭제 | DELETE `/manufacturers/{id}` | ✅ 성공 |
| 7 | Employee 삭제 | DELETE `/employees/{id}` | ✅ 성공 |

---

## 4. 프로필 이미지 API 상세

### Customer 프로필 이미지

#### INSERT (이미지 포함 필수)
```http
POST /api/customers
Content-Type: multipart/form-data

cEmail: string
cPhoneNumber: string
cName: string
cPassword: string
file: UploadFile (이미지 파일)
```

**응답:**
```json
{
  "result": "OK",
  "id": 1
}
```

#### UPDATE (이미지 제외)
```http
PUT /api/customers/{id}
Content-Type: application/json

{
  "cEmail": "updated@test.com",
  "cPhoneNumber": "010-1234-5678",
  "cName": "홍길동",
  "cPassword": "newpassword"
}
```

#### UPDATE (이미지 포함)
```http
POST /api/customers/{id}/with_image
Content-Type: multipart/form-data

customer_id: int
cEmail: string
cPhoneNumber: string
cName: string
cPassword: string
file: UploadFile (이미지 파일)
```

#### 프로필 이미지 조회
```http
GET /api/customers/{id}/profile_image
```

**응답:**
- Content-Type: `image/jpeg`
- Body: 바이너리 이미지 데이터 (Response 객체)

#### 프로필 이미지 삭제
```http
DELETE /api/customers/{id}/profile_image
```

**응답:**
```json
{
  "result": "OK"
}
```

### Employee 프로필 이미지

Employee도 Customer와 동일한 구조를 가집니다:
- POST `/api/employees` (이미지 포함 필수)
- PUT `/api/employees/{id}` (이미지 제외)
- POST `/api/employees/{id}/with_image` (이미지 포함)
- GET `/api/employees/{id}/profile_image` (이미지 조회)
- DELETE `/api/employees/{id}/profile_image` (이미지 삭제)

---

## 5. CRUD 메서드 커버리지

| 기능 | GET | POST | PUT | PATCH | DELETE |
|------|-----|------|-----|-------|--------|
| Customer (고객) | ✅ | ✅ | ✅ | - | ✅ |
| Customer 프로필 이미지 | ✅ | ✅ | ✅ | - | ✅ |
| Employee (직원) | ✅ | ✅ | ✅ | - | ✅ |
| Employee 프로필 이미지 | ✅ | ✅ | ✅ | - | ✅ |
| Manufacturer (제조사) | ✅ | ✅ | - | - | ✅ |
| ProductBase | ✅ | ✅ | - | - | ✅ |
| ProductImage | ✅ | ✅ | ✅ | - | ✅ |
| Product | ✅ | ✅ | - | - | ✅ |
| Purchase (주문) | ✅ | ✅ | ✅ | - | - |
| PurchaseItem (주문 항목) | ✅ | ✅ | ✅ | - | - |
| LoginHistory (로그인 이력) | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 6. 실패 테스트 원인 분석 및 해결

### ✅ 실제 원인: 중복 데이터 문제 (100%)

**초기 분석에서 "모델 검증 필요"라고 추측했으나, 실제로는 모두 중복 데이터 문제였습니다.**

#### 실제 확인된 오류 메시지

1. **고객 정보 수정 (PUT) 실패**
   ```
   (1062, "Duplicate entry 'updated@test.com' for key 'Customer.idx_customer_email'")
   ```
   - **원인**: 하드코딩된 `updated@test.com`이 이미 존재
   - **해결**: 랜덤 이메일 사용 (`updated{rand_num}@test.com`)

2. **주문 생성 (POST) 실패**
   ```
   (1062, "Duplicate entry 'TEST-ORDER-001' for key 'Purchase.idx_purchase_order_code'")
   ```
   - **원인**: 하드코딩된 `TEST-ORDER-001`이 이미 존재
   - **해결**: 랜덤 orderCode 사용 (`TEST-ORDER-{rand_num}`)

3. **ProductBase 생성 실패**
   ```
   (1062, "Duplicate entry 'TEST-001-Red' for key 'ProductBase.idx_productbase_model_color'")
   ```
   - **원인**: 하드코딩된 `TEST-001` + `Red` 조합이 이미 존재
   - **해결**: 랜덤 모델 번호 사용 (`TEST-{rand_num}`)

4. **Employee 필터 테스트 실패**
   - **원인**: 생성 시 `rand_num` 사용했으나 조회 시 하드코딩된 값 사용
   - **해결**: 생성한 데이터(`emp_data`)로 조회하도록 수정

### 해결 방법

1. **테스트 코드 수정**
   - 하드코딩된 값 대신 랜덤 값 사용
   - 생성한 데이터로 조회하도록 수정

2. **데이터베이스 초기화**
   - `init.sql` 실행으로 깨끗한 상태에서 테스트 시작
   - 중복 데이터 제거

### 수정된 테스트 항목

- ✅ Employee 필터 테스트: 생성한 데이터로 조회하도록 수정
- ✅ 고객 정보 수정 (PUT): 랜덤 이메일 사용 (`updated{rand_num}@test.com`)
- ✅ 주문 생성: 랜덤 orderCode 사용 (`TEST-ORDER-{rand_num}`)
- ✅ ProductBase 생성: 랜덤 모델 번호 사용 (`TEST-{rand_num}`)

### 결론

**모든 실패 원인은 중복 데이터 문제였으며, 모델 검증이나 API 로직 문제는 없었습니다.**

### 참고: app_basic_form/app_basic_model은 왜 중복 문제가 없었나?

`app_basic_form`과 `app_basic_model`의 테스트 코드는 다음과 같은 이유로 중복 문제가 없었습니다:

1. **Customer/Employee**: 랜덤 값 사용 (`uid = random.randint(10000, 99999)`)
   ```python
   uid = random.randint(10000, 99999)
   'cEmail': f'test_basic{uid}@test.com'  # 랜덤 값 사용
   ```

2. **ProductBase/Purchase**: 하드코딩이지만 **테스트 후 삭제**
   ```python
   'orderCode': 'TEST-ORDER-001'  # 하드코딩
   # ... 테스트 수행 ...
   api_delete(f'/delete_purchase/{purchase_id}')  # 삭제함!
   ```

3. **각 테스트가 독립적으로 실행**: 테스트 → 삭제 → 다음 테스트

반면 `app/TEST/test_api.py`는:
- 하드코딩된 값 사용 (`updated@test.com`, `TEST-ORDER-001`)
- **삭제하지 않고** 여러 테스트 연속 실행
- → 중복 오류 발생

**교훈**: 테스트 코드는 랜덤 값을 사용하거나, 테스트 후 정리(삭제)를 해야 합니다.

---

## 7. 이미지 처리 방식 변경

### 이전 방식 (base64 인코딩)
```python
# ❌ 옛날 방식
import base64
image_base64 = base64.b64encode(image_data).decode('utf-8')
return {"image": image_base64}
```

### 현재 방식 (Response 객체)
```python
# ✅ 최신 방식
from fastapi import Response
return Response(
    content=image_data,
    media_type="image/jpeg",
    headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
)
```

**장점:**
- 바이너리 데이터 직접 전송 (인코딩 오버헤드 제거)
- 브라우저에서 직접 이미지 표시 가능
- Content-Type 헤더로 이미지 타입 명시
- 캐시 제어 헤더로 항상 최신 이미지 보장

---

## 8. HTTP 메서드 가이드

### 기본 개념

| HTTP 메서드 | SQL | CRUD | 한줄 설명 |
|------------|-----|------|----------|
| **GET** | SELECT | Read | 데이터 **조회** (가져오기) |
| **POST** | INSERT | Create | 데이터 **생성** (새로 만들기) |
| **PUT** | UPDATE | Update | 데이터 **전체 수정** (덮어쓰기) |
| **PATCH** | UPDATE | Update | 데이터 **부분 수정** (일부만 변경) |
| **DELETE** | DELETE | Delete | 데이터 **삭제** (지우기) |

### 🔑 PUT vs PATCH 차이점 (중요!)

#### PUT = 전체 교체 (Replace)
**모든 필드를 다 보내야 합니다.** 안 보낸 필드는 NULL이 됩니다.

```http
PUT /api/customers/1
Content-Type: application/json

{
  "cEmail": "new@test.com",
  "cPhoneNumber": "010-1234-5678",
  "cName": "홍길동",
  "cPassword": "pass123"
}
```

#### PATCH = 부분 수정 (Modify)
**변경할 필드만 보내면 됩니다.** 나머지는 기존 값 유지.

```http
PATCH /api/login_histories/by_customer/1/status?status=logged_out
```

---

## 9. 최적화 API 상세 설명

### 1. `GET /api/product_bases/list/full_detail`

**용도:** 검색/제품 목록 화면

**성능 개선:**
- 기존: 25회 호출 → 개선: 1회 호출 (96% 감소)

### 2. `GET /api/purchases/list/with_items`

**용도:** 주문 목록 화면

**성능 개선:**
- 기존: 6회 호출 → 개선: 1회 호출 (83% 감소)

### 3. `GET /api/purchases/list/with_customer`

**용도:** 관리자 주문 관리 화면

**성능 개선:**
- 기존: 11회 호출 → 개선: 1회 호출 (91% 감소)

---

## 10. Flutter 연동 예시

### Customer 프로필 이미지 업로드 (INSERT)
```dart
import 'package:http/http.dart' as http;
import 'dart:io';

Future<void> createCustomerWithImage() async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/api/customers'),
  );
  
  request.fields['cEmail'] = 'user@test.com';
  request.fields['cPhoneNumber'] = '010-1234-5678';
  request.fields['cName'] = '홍길동';
  request.fields['cPassword'] = 'password123';
  
  var file = await http.MultipartFile.fromPath('file', imagePath);
  request.files.add(file);
  
  var response = await request.send();
  var responseBody = await response.stream.bytesToString();
  print(responseBody);
}
```

### 프로필 이미지 조회
```dart
Future<Uint8List?> getProfileImage(int customerId) async {
  final response = await http.get(
    Uri.parse('$baseUrl/api/customers/$customerId/profile_image'),
  );
  
  if (response.statusCode == 200) {
    return response.bodyBytes;
  }
  return null;
}
```

### Customer 정보 수정 (이미지 포함)
```dart
Future<void> updateCustomerWithImage(int customerId) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('$baseUrl/api/customers/$customerId/with_image'),
  );
  
  request.fields['customer_id'] = customerId.toString();
  request.fields['cEmail'] = 'updated@test.com';
  request.fields['cPhoneNumber'] = '010-9999-8888';
  request.fields['cName'] = '김철수';
  request.fields['cPassword'] = 'newpassword';
  
  var file = await http.MultipartFile.fromPath('file', imagePath);
  request.files.add(file);
  
  var response = await request.send();
}
```

---

## 📊 전체 성능 개선 요약

| 화면 | 기존 호출 | 개선 후 | 감소율 | 사용 API |
|------|----------|---------|--------|----------|
| 검색 화면 | 25회 | 1회 | **96%** | `/product_bases/list/full_detail` |
| 주문 목록 | 6회 | 1회 | **83%** | `/purchases/list/with_items` |
| 관리자 주문 | 11회 | 1회 | **91%** | `/purchases/list/with_customer` |

---

## ✅ 테스트 완료 항목

- ✅ 프로필 이미지 INSERT (Customer/Employee)
- ✅ 프로필 이미지 UPDATE (이미지 제외/포함)
- ✅ 프로필 이미지 조회 (Response 객체)
- ✅ 프로필 이미지 삭제
- ✅ 기본 CRUD API
- ✅ JOIN API
- ✅ 필터링 API
- ✅ 부분 업데이트 API (PATCH)

---

**마지막 업데이트:** 2025-12-27
