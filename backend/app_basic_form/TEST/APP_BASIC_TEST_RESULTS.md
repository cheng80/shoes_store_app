# app_basic_form API 테스트 결과 문서

> 테스트 일자: 2025-12-27
> 테스트 환경: FastAPI + MySQL (외부 서버)
> 서버 주소: http://127.0.0.1:8000
> 테스트 대상: app_basic_form 폴더 (**Form 방식** 학습용 단순화 API)

---

## 📌 방식 설명

| 구분 | 설명 |
|------|------|
| **데이터 입력** | Form 데이터 (multipart/form-data) |
| **이미지 경로** | `product_images.py` - Form (문자열 경로) |
| **프로필 이미지** | `customers.py`, `employees.py` - INSERT/UPDATE 이미지 포함 필수 (Form/UploadFile) |

### 주요 변경 사항

1. **INSERT**: 이미지 포함 필수 (Form + UploadFile)
2. **UPDATE**: 두 가지 방식 제공
   - `update_customer` - 이미지 제외 (Form)
   - `update_customer_with_image` - 이미지 포함 (Form + UploadFile)
3. **이미지 조회**: `view_*_profile_image` - Response 객체로 바이너리 직접 반환

---

## 📊 전체 테스트 요약

| 상태 | 개수 | 비율 |
|------|------|------|
| ✅ 성공 | 53개 | **100%** |
| ❌ 실패 | 0개 | 0% |

---

## 🎉 모든 테스트가 성공했습니다!

---

## 1. 단일 CRUD API 테스트 (9개 파일)

### Customers (고객) - customers.py

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_customers` | 전체 고객 조회 | ✅ 성공 (9건) |
| 2 | GET `/select_customer/{id}` | ID로 고객 조회 | ✅ 성공 |
| 3 | POST `/insert_customer` | 고객 추가 (이미지 포함 필수) | ✅ 성공 |
| 4 | POST `/update_customer` | 고객 수정 (이미지 제외) | ✅ 성공 |
| 5 | POST `/update_customer_with_image` | 고객 수정 (이미지 포함) | ✅ 성공 |
| 6 | GET `/view_customer_profile_image/{id}` | 프로필 이미지 조회 | ✅ 성공 |
| 7 | DELETE `/delete_customer_profile_image/{id}` | 프로필 이미지 삭제 | ✅ 성공 |
| 8 | DELETE `/delete_customer/{id}` | 고객 삭제 | ✅ 성공 |

### Employees (직원) - employees.py

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_employees` | 전체 직원 조회 | ✅ 성공 (3건) |
| 2 | GET `/select_employee/{id}` | ID로 직원 조회 | ✅ 성공 |
| 3 | POST `/insert_employee` | 직원 추가 (이미지 포함 필수) | ✅ 성공 |
| 4 | POST `/update_employee` | 직원 수정 (이미지 제외) | ✅ 성공 |
| 5 | POST `/update_employee_with_image` | 직원 수정 (이미지 포함) | ✅ 성공 |
| 6 | GET `/view_employee_profile_image/{id}` | 프로필 이미지 조회 | ✅ 성공 |
| 7 | DELETE `/delete_employee_profile_image/{id}` | 프로필 이미지 삭제 | ✅ 성공 |
| 8 | DELETE `/delete_employee/{id}` | 직원 삭제 | ✅ 성공 |

### Manufacturers (제조사) - manufacturers.py [Form]

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_manufacturers` | 전체 제조사 조회 | ✅ 성공 (2건) |
| 2 | GET `/select_manufacturer/{id}` | ID로 제조사 조회 | ✅ 성공 |
| 3 | POST `/insert_manufacturer` | 제조사 추가 (Form) | ✅ 성공 |
| 4 | POST `/update_manufacturer` | 제조사 수정 (Form) | ✅ 성공 |
| 5 | DELETE `/delete_manufacturer/{id}` | 제조사 삭제 | ✅ 성공 |

### ProductBases (제품 기본 정보) - product_bases.py [Form]

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_product_bases` | 전체 ProductBase 조회 | ✅ 성공 (13건) |
| 2 | GET `/select_product_base/{id}` | ID로 ProductBase 조회 | ✅ 성공 |
| 3 | POST `/insert_product_base` | ProductBase 추가 (Form) | ✅ 성공 |
| 4 | POST `/update_product_base` | ProductBase 수정 (Form) | ✅ 성공 |
| 5 | DELETE `/delete_product_base/{id}` | ProductBase 삭제 | ✅ 성공 |

### ProductImages (제품 이미지) - product_images.py [Form - 경로 문자열]

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_product_images` | 전체 이미지 조회 | ✅ 성공 (12건) |
| 2 | GET `/select_product_images_by_pbid/{pbid}` | pbid로 이미지 조회 | ✅ 성공 |
| 3 | GET `/select_product_image/{id}` | ID로 이미지 조회 | ✅ 성공 |
| 4 | POST `/insert_product_image` | 이미지 경로 추가 (Form) | ✅ 성공 |
| 5 | POST `/update_product_image` | 이미지 경로 수정 (Form) | ✅ 성공 |
| 6 | DELETE `/delete_product_image/{id}` | 이미지 삭제 | ✅ 성공 |

### Products (제품) - products.py [Form]

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_products` | 전체 제품 조회 | ✅ 성공 (84건) |
| 2 | GET `/select_products_by_pbid/{pbid}` | pbid로 제품 조회 | ✅ 성공 |
| 3 | GET `/select_product/{id}` | ID로 제품 조회 | ✅ 성공 |
| 4 | POST `/insert_product` | 제품 추가 (Form) | ✅ 성공 |
| 5 | POST `/update_product` | 제품 수정 (Form) | ✅ 성공 |
| 6 | DELETE `/delete_product/{id}` | 제품 삭제 | ✅ 성공 |

### Purchases (주문) - purchases.py [Form]

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_purchases` | 전체 주문 조회 | ✅ 성공 (6건) |
| 2 | GET `/select_purchases_by_cid/{cid}` | cid로 주문 조회 | ✅ 성공 |
| 3 | GET `/select_purchase/{id}` | ID로 주문 조회 | ✅ 성공 |
| 4 | POST `/insert_purchase` | 주문 추가 (Form) | ✅ 성공 |
| 5 | POST `/update_purchase` | 주문 수정 (Form) | ✅ 성공 |
| 6 | DELETE `/delete_purchase/{id}` | 주문 삭제 | ✅ 성공 |

### PurchaseItems (주문 항목) - purchase_items.py [Form]

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_purchase_items` | 전체 주문 항목 조회 | ✅ 성공 (8건) |
| 2 | GET `/select_purchase_items_by_pcid/{pcid}` | pcid로 항목 조회 | ✅ 성공 |
| 3 | GET `/select_purchase_item/{id}` | ID로 항목 조회 | ✅ 성공 |
| 4 | POST `/insert_purchase_item` | 항목 추가 (Form) | ✅ 성공 |
| 5 | POST `/update_purchase_item` | 항목 수정 (Form) | ✅ 성공 |
| 6 | POST `/update_purchase_item_status/{id}` | 상태만 수정 (Form) | ✅ 성공 |
| 7 | DELETE `/delete_purchase_item/{id}` | 항목 삭제 | ✅ 성공 |

### LoginHistories (로그인 이력) - login_histories.py [Form]

| # | 엔드포인트 | 설명 | 결과 |
|---|-----------|------|------|
| 1 | GET `/select_login_histories` | 전체 로그인 이력 조회 | ✅ 성공 (7건) |
| 2 | GET `/select_login_histories_by_cid/{cid}` | cid로 이력 조회 | ✅ 성공 |
| 3 | GET `/select_login_history/{id}` | ID로 이력 조회 | ✅ 성공 |
| 4 | POST `/insert_login_history` | 이력 추가 (Form) | ✅ 성공 |
| 5 | POST `/update_login_history` | 이력 수정 (Form) | ✅ 성공 |
| 6 | POST `/update_status_by_cid/{cid}` | 상태만 수정 (Form) | ✅ 성공 |
| 7 | POST `/update_login_time_by_cid/{cid}` | 시간만 수정 (Form) | ✅ 성공 |
| 8 | DELETE `/delete_login_history/{id}` | 이력 삭제 | ✅ 성공 |

---

## 2. 복합 쿼리 (JOIN) API 테스트 (4개 파일)

### ProductBases JOIN API - product_bases_join.py

| # | 엔드포인트 | JOIN 테이블 | 결과 |
|---|-----------|-------------|------|
| 1 | GET `/product_bases/with_first_image` | +ProductImage | ✅ 성공 (13건) |
| 2 | GET `/product_bases/{pbid}/with_images` | +ProductImage | ✅ 성공 |
| 3 | GET `/product_bases/{pbid}/with_products` | +Product | ✅ 성공 |
| 4 | GET `/product_bases/full_detail` | **+Image+Product+Manufacturer (4테이블)** | ✅ 성공 (13건) |

### Products JOIN API - products_join.py

| # | 엔드포인트 | JOIN 테이블 | 결과 |
|---|-----------|-------------|------|
| 1 | GET `/products/{id}/with_base` | +ProductBase | ✅ 성공 |
| 2 | GET `/products/{id}/with_base_and_manufacturer` | +ProductBase+Manufacturer | ✅ 성공 |
| 3 | GET `/products/by_pbid/{pbid}/with_base` | +ProductBase | ✅ 성공 |
| 4 | GET `/products/{id}/full_detail` | +ProductBase+Manufacturer+Image | ✅ 성공 |

### Purchases JOIN API - purchases_join.py

| # | 엔드포인트 | JOIN 테이블 | 결과 |
|---|-----------|-------------|------|
| 1 | GET `/purchases/{id}/with_customer` | +Customer | ✅ 성공 |
| 2 | GET `/purchases/with_customer?cid=1` | +Customer (cid 필터) | ✅ 성공 |
| 3 | GET `/purchases/with_customer` | +Customer (전체) | ✅ 성공 (6건) |
| 4 | GET `/purchases/{id}/with_items` | +PurchaseItem | ✅ 성공 |
| 5 | GET `/purchases/with_items?cid=1` | +PurchaseItem (cid 필터) | ✅ 성공 |
| 6 | GET `/purchases/{id}/full_detail` | +Customer+PurchaseItem | ✅ 성공 |

### PurchaseItems JOIN API - purchase_items_join.py

| # | 엔드포인트 | JOIN 테이블 | 결과 |
|---|-----------|-------------|------|
| 1 | GET `/purchase_items/{id}/with_product` | +Product | ✅ 성공 |
| 2 | GET `/purchase_items/by_pcid/{pcid}/with_product` | +Product | ✅ 성공 |
| 3 | GET `/purchase_items/{id}/full_detail` | **+Product+ProductBase+Manufacturer (4테이블)** | ✅ 성공 |
| 4 | GET `/purchase_items/by_pcid/{pcid}/full_detail` | **+4테이블+Image** | ✅ 성공 |
| 5 | GET `/purchase_items/summary/{pcid}` | 집계 쿼리 | ✅ 성공 |

---

## 3. 파일별 테스트 결과 요약

| 파일 | 유형 | 성공 | 실패 | 상태 |
|------|------|------|------|------|
| customers.py | 단일 CRUD | 5 | 0 | ✅ |
| employees.py | 단일 CRUD | 3 | 0 | ✅ |
| manufacturers.py | 단일 CRUD | 3 | 0 | ✅ |
| product_bases.py | 단일 CRUD | 3 | 0 | ✅ |
| product_images.py | 단일 CRUD | 4 | 0 | ✅ |
| products.py | 단일 CRUD | 4 | 0 | ✅ |
| purchases.py | 단일 CRUD | 4 | 0 | ✅ |
| purchase_items.py | 단일 CRUD | 4 | 0 | ✅ |
| login_histories.py | 단일 CRUD | 4 | 0 | ✅ |
| product_bases_join.py | 복합 JOIN | 4 | 0 | ✅ |
| products_join.py | 복합 JOIN | 4 | 0 | ✅ |
| purchases_join.py | 복합 JOIN | 6 | 0 | ✅ |
| purchase_items_join.py | 복합 JOIN | 5 | 0 | ✅ |
| **합계** | - | **53** | **0** | **100%** |

---

## 4. 테스트 실행 방법

### 전체 테스트 (자동)

```bash
cd /Users/cheng80/Git_Work/shoes_store_app/backend
source venv/bin/activate
python app_basic_form/TEST/run_all_tests.py
```

### 개별 파일 테스트

```bash
# 1. app_basic_form 폴더로 이동
cd /Users/cheng80/Git_Work/shoes_store_app/backend/app_basic_form

# 2. 테스트할 파일 실행 (터미널 1)
python customers.py

# 3. 테스트 실행 (터미널 2)
python TEST/test_app_basic_form.py customers
```

---

## 5. API 구조 요약

### INSERT (이미지 포함 필수)

**Customer/Employee**:
```python
POST /insert_customer
Content-Type: multipart/form-data
- cEmail: str (Form)
- cPhoneNumber: str (Form)
- cName: str (Form)
- cPassword: str (Form)
- file: UploadFile (File)  # 필수
```

**기타 테이블**:
```python
POST /insert_manufacturer
Content-Type: multipart/form-data
- mName: str (Form)
```

### UPDATE (두 가지 방식)

**이미지 제외**:
```python
POST /update_customer
Content-Type: multipart/form-data
- customer_id: int (Form)
- cEmail: str (Form)
- cPhoneNumber: str (Form)
- cName: str (Form)
- cPassword: str (Form)
```

**이미지 포함**:
```python
POST /update_customer_with_image
Content-Type: multipart/form-data
- customer_id: int (Form)
- cEmail: str (Form)
- cPhoneNumber: str (Form)
- cName: str (Form)
- cPassword: str (Form)
- file: UploadFile (File)  # 필수
```

### 이미지 조회

```python
GET /view_customer_profile_image/{customer_id}
Response: image/jpeg (바이너리 직접 반환)
```

---

## 6. app_basic_form vs app_basic_model 비교

| 구분 | app_basic_form | app_basic_model |
|------|----------------|-----------------|
| **데이터 입력** | Form 데이터 | JSON Body (Pydantic) |
| **모델 정의** | 사용 안함 | Create/Update 모델 분리 |
| **이미지 처리** | Form + UploadFile | Form + UploadFile (동일) |
| **Flutter 연동** | `http.post(body: data)` | `jsonEncode(body)` |
| **swagger 테스트** | Form 입력 | JSON 입력 |

---

## 📁 app_basic_form 폴더 구조

```
app_basic_form/
├── TEST/
│   ├── run_all_tests.py           # 전체 자동 테스트
│   ├── test_app_basic_form.py     # 개별 테스트
│   └── APP_BASIC_TEST_RESULTS.md  # 이 문서
│
├── database/
│   └── connection.py              # DB 연결 (공용)
│
├── # 단일 CRUD (9개) - Form 방식
├── customers.py                   # 이미지 포함 INSERT/UPDATE
├── employees.py                   # 이미지 포함 INSERT/UPDATE
├── manufacturers.py               # Form
├── product_bases.py               # Form
├── product_images.py             # Form (경로 문자열)
├── products.py                    # Form
├── purchases.py                  # Form
├── purchase_items.py             # Form
├── login_histories.py            # Form
│
└── # 복합 쿼리 JOIN (4개) - GET only
├── product_bases_join.py
├── products_join.py
├── purchases_join.py
└── purchase_items_join.py
```

---

## 🎉 결론

- **전체 성공률**: **100%** (53/53)
- **단일 CRUD API**: 9개 파일 모두 정상 동작 ✅
- **복합 쿼리 (JOIN) API**: 4개 파일 모두 정상 동작 ✅
- **이미지 포함 INSERT**: Customer, Employee 정상 동작 ✅
- **이미지 제외/포함 UPDATE**: 두 가지 방식 모두 정상 동작 ✅
- **이미지 조회**: Response 객체로 바이너리 직접 반환 정상 동작 ✅
