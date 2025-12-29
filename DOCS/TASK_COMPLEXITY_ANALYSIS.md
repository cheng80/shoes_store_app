# 담당자별 작업 복잡도 상세 분석

**작성일**: 2025-01-XX  
**목적**: 담당자별 작업 복잡도를 상세히 분석하여 로그인 히스토리 협업 방안 결정

---

## 📊 담당자별 작업 복잡도 분석

### 담당자 1: 로그인 및 개인정보 수정

| 항목 | 내용 |
|------|------|
| **화면 수** | 6개 |
| **복잡도** | 낮음 |
| **주요 작업** | 단순 CRUD 작업 |
| **기술 스택** | MySQL, FastAPI |
| **특징** | 로직이 단순하고 반복적 |

**담당 화면:**
- 사용자 로그인 (단순 인증)
- 사용자 메뉴 드로어 (단순 조회)
- 사용자-회원가입 (단순 INSERT)
- 사용자-개인정보 수정 (단순 UPDATE)
- 관리자-로그인 (단순 인증)
- 관리자-드로어 메뉴 (단순 조회)
- 관리자-개인정보 수정 (단순 UPDATE)

---

### 담당자 2: 상품 조회 및 상세 화면 ⚠️

| 항목 | 내용 |
|------|------|
| **화면 수** | 2개 |
| **복잡도** | **매우 높음** |
| **주요 작업** | 복잡한 JOIN 쿼리, 필터링 로직 |
| **기술 스택** | MySQL, FastAPI, 복잡한 쿼리 최적화 |
| **특징** | 화면 수는 적지만 복잡도가 가장 높음 |

**담당 화면:**

#### 1. 사용자-상품조회
- **필요 테이블**: 6개 테이블 JOIN
  - `product`
  - `kind_category`
  - `color_category`
  - `size_category`
  - `gender_category`
  - `maker`
- **개발 API**:
  - `GET /api/products/with_categories` - 모든 카테고리 정보 포함 조회
  - `GET /api/products/by_category` - 카테고리별 필터링
  - `GET /api/products/by_maker/{maker_seq}/with_categories` - 제조사별 조회
  - `GET /api/makers` - 제조사 목록
  - `GET /api/kind_categories` - 종류 카테고리 목록
  - `GET /api/color_categories` - 색상 카테고리 목록
  - `GET /api/size_categories` - 사이즈 카테고리 목록
  - `GET /api/gender_categories` - 성별 카테고리 목록
- **복잡도 요인**:
  - 6개 테이블 JOIN 최적화
  - 다중 카테고리 필터링 로직
  - 제조사별 필터링 로직
  - 카테고리별 조합 필터링
  - 쿼리 성능 최적화 필요

#### 2. 상품상세화면
- **필요 테이블**: 6개 테이블 JOIN
  - `product` + 모든 카테고리 테이블 + `maker`
- **개발 API**:
  - `GET /api/products/{p_seq}/full_detail` - 모든 정보 포함 상세 조회
- **복잡도 요인**:
  - 6개 테이블 JOIN
  - 모든 카테고리 정보 포함
  - 제조사 정보 포함

**총 복잡도: 매우 높음** ⚠️
- 화면 수는 적지만 (2개)
- 6개 테이블 JOIN 작업
- 다수의 필터링 API 개발 필요
- 쿼리 최적화 필요

---

### 담당자 3: 장바구니, 주문, 결제 프로세스

| 항목 | 내용 |
|------|------|
| **화면 수** | 4개 |
| **복잡도** | 높음 |
| **주요 작업** | 트랜잭션 처리, 재고 관리, 결제 로직 |
| **기술 스택** | MySQL, FastAPI, 트랜잭션 처리 |
| **특징** | 비즈니스 로직이 복잡함 |

**담당 화면:**
- 사용자-장바구니 (임시 저장, 재고 확인)
- 사용자-주소:결제방법 (지점 선택)
- 사용자-결제팝업 (재고 확인)
- 사용자-결제하기 (트랜잭션 처리, 재고 차감)

**복잡도 요인:**
- 트랜잭션 처리
- 재고 동시성 제어
- 결제 프로세스 로직
- 장바구니 임시 저장 로직

---

### 담당자 4: 사용자 주문, 수령/반품 조회 ⭐

| 항목 | 내용 |
|------|------|
| **화면 수** | 4개 |
| **복잡도** | 높음 |
| **주요 작업** | 조회 화면 개발, JOIN 쿼리 |
| **기술 스택** | MySQL, FastAPI |
| **특징** | 조회 화면 개발 경험 보유 |

**담당 화면:**

#### 1. 사용자- 주문내역 조회
- **필요 테이블**: 3개 테이블 JOIN
  - `purchase_item`, `product`, `branch`
- **개발 API**:
  - `GET /api/purchase_items/by_user/{user_seq}/orders`
  - `GET /api/purchase_items/by_user/{user_seq}/with_details`

#### 2. 사용자- 주문내역 조회(상세화면)
- **필요 테이블**: 10개 테이블 JOIN
  - `purchase_item`, `user`, `product`, `branch`, `pickup`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker`
- **개발 API**:
  - `GET /api/purchase_items/by_tnum/{b_tnum}/with_details`
  - `GET /api/purchase_items/{b_seq}/full_detail`
  - `GET /api/pickups/by_purchase/{b_seq}`

#### 3. 사용자-수령 반품목록 조회
- **필요 테이블**: 6개 테이블 JOIN
  - `pickup`, `purchase_item`, `product`, `branch`, `refund`, `staff`
- **개발 API**:
  - `GET /api/pickups/by_user/{user_seq}/with_details`
  - `GET /api/refunds/by_user/{user_seq}/with_details`

#### 4. 사용자-수령 반품목록 조회(상세화면)
- **필요 테이블**: 10개 테이블 JOIN
  - `pickup`, `purchase_item`, `product`, `branch`, `refund`, `staff`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker`
- **개발 API**:
  - `GET /api/pickups/{pic_seq}/full_detail`
  - `GET /api/refunds/{refund_seq}/full_detail`
  - `POST /api/refunds`

**복잡도 요인:**
- 다수의 조회 화면 개발
- JOIN 쿼리 작성 경험
- 조회 API 개발 패턴 숙지

**SQLite 로그인 히스토리 작업과의 유사성:**
- ✅ 조회 화면 개발 경험 보유
- ✅ JOIN 쿼리 작성 경험
- ✅ 조회 API 개발 패턴 유사
- ✅ 주문/반품 조회 작업 완료 후 여유 생길 가능성

---

### 담당자 5: 관리자 주문, 수령/반품 관리

| 항목 | 내용 |
|------|------|
| **화면 수** | 4개 |
| **복잡도** | 높음 |
| **주요 작업** | 관리자용 조회/관리 화면 |
| **기술 스택** | MySQL, FastAPI |
| **특징** | 사용자용과 유사하지만 관리 기능 추가 |

**담당 화면:**
- 관리자-주문목록 조회
- 관리자-주문목록 조회(상세화면)
- 관리자-반품목록 조회
- 관리자-반품목록 조회(상세화면)

**복잡도 요인:**
- 관리자용 필터링 로직
- 수령/반품 처리 로직

---

## 🎯 로그인 히스토리 협업 방안 재분석

### 담당자 2 제외 이유

**화면 수는 적지만 복잡도 매우 높음:**
- 6개 테이블 JOIN 작업
- 카테고리별 필터링 API 다수 개발 필요
- 제조사별 조회 API 개발 필요
- 쿼리 최적화 필요
- **SQLite 작업 추가 시 과부하 가능성 매우 높음** ⚠️

### 담당자 4 권장 이유 ⭐

**조회 화면 개발 경험 보유:**
- 주문/반품 조회 화면 개발 경험
- JOIN 쿼리 작성 경험
- 조회 API 개발 패턴 숙지

**SQLite 작업과의 유사성:**
- 조회 화면 개발 패턴 유사
- JOIN 쿼리 작성 경험 활용 가능
- 주문/반품 조회 작업 완료 후 여유 생길 가능성

**작업량 분산 효과:**
- 담당자 1: 로그인 API 수정만 (1-2일)
- 담당자 4: SQLite 작업 + 조회 화면 (3-4일)
- 작업량 분산 효과적

---

## 📋 최종 권장안

### 협업 방식

**1단계: 담당자 1 (로그인 API 수정)**
- 로그인 성공 시 SQLite 기록 호출 추가
- 해시 처리 로직 구현
- **예상 기간**: 1-2일

**2단계: 담당자 4 (SQLite 작업 + 조회 화면)**
- SQLite 스키마 설계 및 구현
- 로그인 히스토리 조회 API 개발
- 로그인 히스토리 조회 화면 개발
- **예상 기간**: 3-4일

**협업 포인트:**
- 담당자 1이 해시 처리 로직과 API 호출 방식을 담당자 4와 공유
- 담당자 4가 SQLite 스키마와 조회 API를 개발 (주문/반품 조회와 유사한 패턴)
- 담당자 1이 로그인 API에 통합

---

## 🎯 결론

**담당자 2는 제외:**
- 화면 수는 적지만 복잡도 매우 높음
- 6개 테이블 JOIN 작업
- 카테고리 필터링 API 다수 개발 필요
- SQLite 작업 추가 시 과부하 가능성 매우 높음

**담당자 4와 협업 권장:**
- 조회 화면 개발 경험 보유
- SQLite 작업과 유사한 패턴
- 주문/반품 조회 작업 완료 후 여유 생길 가능성
- 작업량 분산 효과적

---

## 📚 참고 문서

- 로그인 히스토리 작업량 분석: `LOGIN_HISTORY_WORKLOAD_ANALYSIS.md`
- 작업 분담 분석: `WORKLOAD_ANALYSIS.md`
- 최종 작업 분담: `TASK_DISTRIBUTION_FINAL.md`

