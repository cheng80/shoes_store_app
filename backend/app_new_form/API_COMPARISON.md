# 신규 API 구조 vs 기존 API 구조 비교 분석

**작성일**: 2025-01-XX  
**비교 대상**:
- 기존: `backend/app_basic_form` (기존 ERD 구조)
- 신규: `backend/app_new_form` (새로운 ERD 구조)

---

## 📊 전체 구조 비교

### 기존 API 구조 (app_basic_form)

| 테이블 | API 파일 | 엔드포인트 |
|--------|---------|-----------|
| Customer | customers.py | `/api/customers` |
| Employee | employees.py | `/api/employees` |
| Manufacturer | manufacturers.py | `/api/manufacturers` |
| ProductBase | product_bases.py | `/api/product_bases` |
| ProductImage | product_images.py | `/api/product_images` |
| Product | products.py | `/api/products` |
| Purchase | purchases.py | `/api/purchases` |
| PurchaseItem | purchase_items.py | `/api/purchase_items` |
| LoginHistory | login_histories.py | `/api/login_histories` |

**총 9개 기본 CRUD API + 4개 JOIN API**

### 신규 API 구조 (app_new_form)

| 테이블 | API 파일 | 엔드포인트 |
|--------|---------|-----------|
| branch | branch.py | `/api/branches` |
| user | users.py | `/api/users` |
| staff | staff.py | `/api/staffs` |
| maker | maker.py | `/api/makers` |
| kind_category | kind_category.py | `/api/kind_categories` |
| color_category | color_category.py | `/api/color_categories` |
| size_category | size_category.py | `/api/size_categories` |
| gender_category | gender_category.py | `/api/gender_categories` |
| product | product.py | `/api/products` |
| purchase_item | purchase_item.py | `/api/purchase_items` |
| pickup | pickup.py | `/api/pickups` |
| refund | refund.py | `/api/refunds` |
| receive | receive.py | `/api/receives` |
| request | request.py | `/api/requests` |

**총 14개 기본 CRUD API + 6개 JOIN API**

---

## 🔄 주요 변경사항

### 1. 테이블 구조 변경

#### 1.1 고객/직원 계정 구조

**기존 구조:**
```
Customer (고객)
├─ id (PK)
├─ cEmail (이메일)
├─ cPhoneNumber
├─ cName
├─ cPassword
└─ cProfileImage

Employee (직원)
├─ id (PK)
├─ eEmail (이메일)
├─ ePhoneNumber
├─ eName
├─ ePassword
├─ eRole
└─ eProfileImage
```

**신규 구조:**
```
user (고객)
├─ u_seq (PK)
├─ u_id (로그인 ID) ← 이메일 대신 ID 사용
├─ u_password
├─ u_name
├─ u_phone
└─ u_image

staff (직원)
├─ s_seq (PK)
├─ br_seq (FK → branch) ← 지점 연결 추가
├─ s_password
├─ s_phone
├─ s_rank
├─ s_superseq (상급자 참조)
└─ s_image

branch (지점) ← 신규 추가
├─ br_seq (PK)
├─ br_name
├─ br_phone
├─ br_address
├─ br_lat
└─ br_lng
```

**변경 사항:**
- ✅ `Customer` → `user`: 이메일 기반 → ID 기반 인증
- ✅ `Employee` → `staff`: 지점 연결 추가, 상급자 참조 추가
- ✅ `branch` 테이블 신규 추가 (지점 정보 관리)

#### 1.2 제품 구조

**기존 구조:**
```
ProductBase (제품 기본 정보)
├─ id (PK)
├─ pName
├─ pDescription
├─ pColor
├─ pGender
├─ pStatus
├─ pCategory
└─ pModelNumber

Product (제품 - 사이즈별)
├─ id (PK)
├─ pbid (FK → ProductBase)
├─ mfid (FK → Manufacturer)
├─ size
├─ basePrice
└─ pQuantity

ProductImage (제품 이미지)
├─ id (PK)
├─ pbid (FK → ProductBase)
└─ imagePath
```

**신규 구조:**
```
product (제품 - 통합)
├─ p_seq (PK)
├─ kc_seq (FK → kind_category)
├─ cc_seq (FK → color_category)
├─ sc_seq (FK → size_category)
├─ gc_seq (FK → gender_category)
├─ m_seq (FK → maker)
├─ p_name
├─ p_price
├─ p_stock
└─ p_image (VARCHAR - 경로 문자열)

kind_category (종류 카테고리) ← 신규
├─ kc_seq (PK)
└─ kc_name

color_category (색상 카테고리) ← 신규
├─ cc_seq (PK)
└─ cc_name

size_category (사이즈 카테고리) ← 신규
├─ sc_seq (PK)
└─ sc_name

gender_category (성별 카테고리) ← 신규
├─ gc_seq (PK)
└─ gc_name
```

**변경 사항:**
- ✅ `ProductBase` + `Product` → `product` (단일 테이블로 통합)
- ✅ `ProductImage` → `product.p_image` (별도 테이블 제거, 경로 문자열로 저장)
- ✅ 카테고리 분리: 색상, 성별, 종류, 사이즈를 별도 테이블로 분리 (정규화)
- ✅ 제조사: `Manufacturer` → `maker`

#### 1.3 주문 구조

**기존 구조:**
```
Purchase (주문)
├─ id (PK)
├─ cid (FK → Customer)
├─ pickupDate
├─ orderCode
└─ timeStamp

PurchaseItem (주문 항목)
├─ id (PK)
├─ pid (FK → Product)
├─ pcid (FK → Purchase)
├─ pcQuantity
└─ pcStatus
```

**신규 구조:**
```
purchase_item (구매 내역 - 통합)
├─ b_seq (PK)
├─ br_seq (FK → branch) ← 지점 정보 추가
├─ u_seq (FK → user)
├─ p_seq (FK → product)
├─ b_price
├─ b_quantity
├─ b_date
└─ b_tnum ← 주문 그룹화 번호 (신규)
```

**변경 사항:**
- ✅ `Purchase` + `PurchaseItem` → `purchase_item` (단일 테이블로 통합)
- ✅ `b_tnum` 필드 추가: 여러 구매 항목을 하나의 주문으로 그룹화
- ✅ 지점 정보 추가: `br_seq` (어느 지점에서 구매했는지)
- ✅ 주문 상태 제거: `pcStatus` 필드 제거

#### 1.4 신규 기능 테이블

**신규 추가된 테이블:**
```
pickup (수령)
├─ pic_seq (PK)
├─ b_seq (FK → purchase_item)
└─ pic_date

refund (반품)
├─ ref_seq (PK)
├─ ref_date
├─ ref_reason
├─ u_seq (FK → user)
├─ s_seq (FK → staff)
└─ pic_seq (FK → pickup)

receive (입고)
├─ rec_seq (PK)
├─ rec_quantity
├─ rec_date
├─ s_seq (FK → staff)
├─ p_seq (FK → product)
└─ m_seq (FK → maker)

request (발주)
├─ req_seq (PK)
├─ req_date
├─ req_content
├─ req_quantity
├─ req_manappdate (팀장 결재일)
├─ req_dirappdate (이사 결재일)
├─ s_seq (FK → staff)
├─ p_seq (FK → product)
├─ m_seq (FK → maker)
└─ s_superseq (FK → staff, 상급자)
```

**기존에 없던 기능:**
- ✅ 오프라인 수령 관리 (`pickup`)
- ✅ 반품/환불 관리 (`refund`)
- ✅ 입고 관리 (`receive`)
- ✅ 발주/품의 관리 (`request`) - 결재 프로세스 포함

---

## 🔍 상세 비교

### 2. 필드명 명명 규칙 변경

| 구분 | 기존 | 신규 | 변경 이유 |
|------|------|------|----------|
| 기본 키 | `id` | `{table}_seq` | 테이블명 명시로 가독성 향상 |
| 외래 키 | `{table}id` | `{table}_seq` | 일관성 유지 |
| 고객 ID | `cid` | `u_seq` | 명확한 테이블 참조 |
| 제품 ID | `pid`, `pbid` | `p_seq` | 단일 테이블로 통합 |
| 제조사 ID | `mfid` | `m_seq` | 일관성 유지 |
| 직원 ID | `eid` | `s_seq` | 일관성 유지 |

### 3. 데이터 모델 변경

#### 3.1 고객 모델

**기존:**
```python
class Customer(BaseModel):
    id: Optional[int] = None
    cEmail: str          # 이메일 기반
    cPhoneNumber: str
    cName: str
    cPassword: str
```

**신규:**
```python
class User(BaseModel):
    u_seq: Optional[int] = None
    u_id: str            # ID 기반 (이메일 아님)
    u_password: str
    u_name: str
    u_phone: str
```

**변경 사항:**
- 이메일 기반 → ID 기반 인증
- 필드명 카멜케이스 → 스네이크케이스

#### 3.2 제품 모델

**기존:**
```python
class ProductBase(BaseModel):
    id: Optional[int] = None
    pName: str
    pDescription: str
    pColor: str          # 문자열
    pGender: str         # 문자열
    pCategory: str
    pModelNumber: str

class Product(BaseModel):
    id: Optional[int] = None
    pbid: Optional[int] = None  # ProductBase 참조
    mfid: Optional[int] = None  # Manufacturer 참조
    size: int
    basePrice: int
    pQuantity: int
```

**신규:**
```python
class Product(BaseModel):
    p_seq: Optional[int] = None
    kc_seq: int          # kind_category 참조
    cc_seq: int          # color_category 참조
    sc_seq: int          # size_category 참조
    gc_seq: int          # gender_category 참조
    m_seq: int           # maker 참조
    p_name: Optional[str] = None
    p_price: int = 0
    p_stock: int = 0
    p_image: Optional[str] = None  # 경로 문자열
```

**변경 사항:**
- 두 테이블 통합 → 단일 테이블
- 카테고리 문자열 → 외래 키 참조 (정규화)
- 이미지 별도 테이블 → 경로 문자열

#### 3.3 주문 모델

**기존:**
```python
class Purchase(BaseModel):
    id: Optional[int] = None
    cid: Optional[int] = None
    pickupDate: str
    orderCode: str
    timeStamp: str

class PurchaseItem(BaseModel):
    id: Optional[int] = None
    pid: Optional[int] = None
    pcid: Optional[int] = None  # Purchase 참조
    pcQuantity: int
    pcStatus: str
```

**신규:**
```python
class PurchaseItem(BaseModel):
    b_seq: Optional[int] = None
    br_seq: int          # branch 참조
    u_seq: int           # user 참조
    p_seq: int           # product 참조
    b_price: int = 0
    b_quantity: int = 1
    b_date: datetime
    b_tnum: Optional[str] = None  # 주문 그룹화 번호
```

**변경 사항:**
- 두 테이블 통합 → 단일 테이블
- `orderCode` → `b_tnum` (주문 그룹화)
- 주문 상태 제거
- 지점 정보 추가

### 4. API 엔드포인트 구조 변경

#### 4.1 RESTful 경로 구조

**기존:**
```
GET  /api/customers              # 전체 조회
GET  /api/customers/{id}         # ID 조회
POST /api/customers              # 추가
POST /api/customers/{id}         # 수정
POST /api/customers/{id}/with_image  # 이미지 포함 수정
GET  /api/customers/{id}/profile_image  # 이미지 조회
DELETE /api/customers/{id}/profile_image  # 이미지 삭제
DELETE /api/customers/{id}       # 삭제
```

**신규:**
```
GET  /api/users                  # 전체 조회
GET  /api/users/{user_seq}       # ID 조회
POST /api/users                  # 추가
POST /api/users/{user_seq}       # 수정
POST /api/users/{user_seq}/with_image  # 이미지 포함 수정
GET  /api/users/{user_seq}/profile_image  # 이미지 조회
DELETE /api/users/{user_seq}/profile_image  # 이미지 삭제
DELETE /api/users/{user_seq}     # 삭제
```

**변경 사항:**
- 경로 구조는 동일 (RESTful 유지)
- 파라미터명 변경: `{id}` → `{user_seq}` 등

#### 4.2 특수 엔드포인트

**기존:**
```
GET /api/products/{id}/with_base      # Product + ProductBase
GET /api/purchases/{id}/with_customer # Purchase + Customer
GET /api/purchases/{id}/with_items    # Purchase + PurchaseItems
```

**신규:**
```
GET /api/products/{p_seq}/full_detail        # Product + 모든 카테고리 + Maker
GET /api/purchase_items/{b_seq}/with_details # PurchaseItem + User + Product + Branch
GET /api/purchase_items/{b_seq}/full_detail # PurchaseItem + 모든 관련 정보
GET /api/purchase_items/by_tnum/{b_tnum}/with_details  # b_tnum으로 그룹화된 주문
```

**변경 사항:**
- JOIN 쿼리 구조 변경 (더 많은 테이블 조인)
- `b_tnum` 기반 주문 그룹화 API 추가

### 5. JOIN API 구조 변경

#### 5.1 기존 JOIN API

**products_join.py:**
- `Product` + `ProductBase` + `Manufacturer`
- 최대 3개 테이블 조인

**purchases_join.py:**
- `Purchase` + `Customer`
- `Purchase` + `PurchaseItem`
- 최대 3개 테이블 조인

**purchase_items_join.py:**
- `PurchaseItem` + `Product` + `ProductBase` + `Manufacturer`
- 최대 4개 테이블 조인

#### 5.2 신규 JOIN API

**product_join.py:**
- `Product` + `KindCategory` + `ColorCategory` + `SizeCategory` + `GenderCategory` + `Maker`
- **최대 6개 테이블 조인**

**purchase_item_join.py:**
- `PurchaseItem` + `User` + `Product` + `Branch` + 모든 카테고리
- **최대 9개 테이블 조인**

**refund_join.py:**
- `Refund` + `User` + `Staff` + `Pickup` + `PurchaseItem` + `Product` + `Branch` + 모든 카테고리
- **최대 12개 테이블 조인**

**변경 사항:**
- 더 복잡한 JOIN 구조
- 카테고리 테이블 추가로 조인 테이블 수 증가

---

## 📈 기능적 차이점

### 6. 새로운 기능

#### 6.1 주문 그룹화 (`b_tnum`)

**기존:**
- `Purchase` 테이블로 주문 그룹화
- `PurchaseItem`이 `Purchase`를 참조

**신규:**
- `b_tnum` 필드로 주문 그룹화
- 여러 `purchase_item`이 같은 `b_tnum`을 가짐
- 하나의 주문에 여러 항목 포함 가능

**예시:**
```sql
-- 같은 b_tnum을 가진 항목들이 하나의 주문
SELECT * FROM purchase_item WHERE b_tnum = 'TXN0001';
-- 결과: 3개 항목 (신발 2개, 양말 1개)
```

#### 6.2 지점 관리

**기존:**
- 지점 정보 없음
- 직원이 지점에 소속되지 않음

**신규:**
- `branch` 테이블 추가
- 직원이 지점에 소속 (`staff.br_seq`)
- 구매 내역에 지점 정보 포함 (`purchase_item.br_seq`)

#### 6.3 카테고리 관리

**기존:**
- 제품 속성이 문자열로 저장
- 색상, 성별, 종류가 제품 테이블에 직접 저장

**신규:**
- 카테고리를 별도 테이블로 분리
- 정규화로 데이터 중복 제거
- 카테고리 추가/수정 용이

#### 6.4 비즈니스 프로세스 관리

**신규 추가:**
- **수령 관리** (`pickup`): 오프라인 수령 처리
- **반품 관리** (`refund`): 반품/환불 처리
- **입고 관리** (`receive`): 제품 입고 처리
- **발주 관리** (`request`): 발주 및 결재 프로세스

---

## 🎯 개선 사항 요약

### 7. 데이터베이스 설계 개선

| 항목 | 기존 | 신규 | 개선 효과 |
|------|------|------|----------|
| **정규화** | 부분적 | 완전 | 데이터 중복 제거 |
| **확장성** | 제한적 | 우수 | 카테고리 추가 용이 |
| **유연성** | 낮음 | 높음 | 비즈니스 프로세스 추가 가능 |
| **성능** | 보통 | 향상 | 인덱스 추가, 조인 최적화 |

### 8. API 구조 개선

| 항목 | 기존 | 신규 | 개선 효과 |
|------|------|------|----------|
| **테이블 수** | 9개 | 14개 | 기능 확장 |
| **JOIN API** | 4개 | 6개 | 더 복잡한 쿼리 지원 |
| **엔드포인트** | ~50개 | ~70개 | 기능 확장 |
| **명명 규칙** | 혼재 | 일관성 | 가독성 향상 |

---

## 📝 주요 차이점 요약

### 구조적 차이

1. **테이블 통합**
   - `ProductBase` + `Product` → `product`
   - `Purchase` + `PurchaseItem` → `purchase_item`

2. **테이블 분리**
   - 카테고리 4개 테이블로 분리
   - 이미지 테이블 제거 (경로 문자열로 저장)

3. **신규 테이블 추가**
   - `branch` (지점)
   - `pickup`, `refund`, `receive`, `request` (비즈니스 프로세스)

### 기능적 차이

1. **주문 그룹화**
   - 기존: `Purchase` 테이블
   - 신규: `b_tnum` 필드

2. **지점 관리**
   - 기존: 없음
   - 신규: 완전한 지점 관리 시스템

3. **비즈니스 프로세스**
   - 기존: 기본 CRUD만
   - 신규: 수령, 반품, 입고, 발주 프로세스 포함

### 기술적 차이

1. **명명 규칙**
   - 기존: 카멜케이스 (`cEmail`, `pName`)
   - 신규: 스네이크케이스 (`u_id`, `p_name`)

2. **인증 방식**
   - 기존: 이메일 기반
   - 신규: ID 기반

3. **JOIN 복잡도**
   - 기존: 최대 4개 테이블
   - 신규: 최대 12개 테이블

---

## 🔄 마이그레이션 고려사항

### 데이터 마이그레이션 필요

1. **고객 데이터**
   - `Customer.cEmail` → `user.u_id` (이메일을 ID로 사용 가능)
   - 필드명 매핑 필요

2. **제품 데이터**
   - `ProductBase` + `Product` → `product` 통합
   - 카테고리 문자열 → 카테고리 테이블 참조로 변환

3. **주문 데이터**
   - `Purchase` + `PurchaseItem` → `purchase_item` 통합
   - `Purchase.orderCode` → `purchase_item.b_tnum`

### API 호환성

- **호환되지 않음**: 완전히 다른 구조이므로 API 마이그레이션 필요
- **클라이언트 코드 수정 필요**: 모든 엔드포인트 변경

---

## ✅ 결론

신규 API 구조는 기존 구조 대비:

1. **더 정규화된 구조**: 카테고리 분리로 데이터 중복 제거
2. **더 많은 기능**: 지점 관리, 비즈니스 프로세스 추가
3. **더 유연한 확장성**: 카테고리 추가/수정 용이
4. **더 복잡한 JOIN**: 최대 12개 테이블 조인 지원
5. **일관된 명명 규칙**: 스네이크케이스로 통일

**전체적으로 더 엔터프라이즈급 구조로 발전**

