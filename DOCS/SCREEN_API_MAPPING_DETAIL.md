# 화면별 개발 가이드 - 상세 버전

**작성일**: 2025-01-XX  
**목적**: 화면 개발 시 필요한 DB 테이블, 컬럼, API 상세 정보

---

## 📋 작업 분담 (최종)

| 담당자 | 담당 화면 수 | 주요 기능 | 복잡도 |
|--------|------------|----------|--------|
| **담당자 1** | 6개 | 사용자/관리자 로그인 및 개인정보 수정 | 낮음 |
| **담당자 2** | 2개 | 상품 조회 및 상세 화면 | 중간 |
| **담당자 3** | 4개 | 장바구니, 주문, 결제 프로세스 | 높음 |
| **담당자 4** | 4개 | 사용자 주문, 수령/반품 조회 | 높음 |
| **담당자 5** | 4개 | 관리자 주문, 수령/반품 관리 | 높음 |
| **담당자 6** | - | PM 및 디테일 페이지 3D 프리뷰 | - |

**총 화면 수:** 20개  
**평균 화면 수:** 4.0개/인 (담당자 6 제외)

**참고**: 
- 작업 분담 분석: `WORKLOAD_ANALYSIS.md` 파일 참조
- 데이터 중복성 분석: `DATA_DUPLICATION_ANALYSIS.md` 파일 참조
  - 주문/반품 조회는 사용자용과 관리자용이 거의 동일한 데이터 사용
  - 담당자 4와 5는 협업하여 공통 API를 먼저 개발하고 필터링 조건만 추가하는 것을 권장
- 장바구니는 DB 테이블 없이 임시 저장(메모리/로컬스토리지)으로만 사용
- 로그인과 개인정보 수정은 사용자/관리자 모두 비슷한 로직 (단순)

---

## 관리자 화면

### 1. 관리자-로그인

| 항목 | 내용 |
|------|------|
| **화면 설명** | 관리자(직원) 로그인 화면 |
| **주요 기능** | ID/PW로 로그인 인증 |
| **담당자** | 담당자 1 |
| **필요 DB 테이블** | `staff` |
| **필요 컬럼** | `s_phone`, `s_password` |
| **개발 API** | `POST /api/staffs/login` |
| **참고** | 사용자 로그인과 비슷한 로직 (ID/PW 확인만), 관리자 화면은 태블릿용이지만 로직은 동일

---

### 2. 관리자-드로어 메뉴

| 항목 | 내용 |
|------|------|
| **화면 설명** | 관리자 메뉴 네비게이션 |
| **주요 기능** | 현재 로그인한 직원 정보 표시 |
| **담당자** | 담당자 1 |
| **필요 DB 테이블** | `staff` |
| **필요 컬럼** | `s_seq`, `s_rank`, `s_phone`, `s_image` |
| **개발 API** | `GET /api/staffs/{staff_seq}`, `GET /api/staffs/{staff_seq}/profile_image` |
| **참고** | 사용자 메뉴 드로어와 비슷한 로직, 관리자 화면은 태블릿용이지만 로직은 동일

---

### 3. 관리자-개인정보 수정

| 항목 | 내용 |
|------|------|
| **화면 설명** | 관리자 개인정보 수정 화면 |
| **주요 기능** | 직원 정보 조회/수정, 프로필 이미지 관리 |
| **담당자** | 담당자 1 |
| **필요 DB 테이블** | `staff`, `branch` |
| **필요 컬럼** | `staff`: `s_seq`, `br_seq`, `s_password`, `s_rank`, `s_phone`, `s_image`<br>`branch`: `br_seq`, `br_name` |
| **개발 API** | `GET /api/staffs/{staff_seq}`, `GET /api/staffs/{staff_seq}/profile_image`<br>`POST /api/staffs/{staff_seq}`, `POST /api/staffs/{staff_seq}/with_image`<br>`DELETE /api/staffs/{staff_seq}/profile_image`<br>`GET /api/branches` |
| **참고** | 사용자 개인정보 수정과 비슷한 로직 (단순 CRUD)

---

### 4. 관리자-주문목록 조회

| 항목 | 내용 |
|------|------|
| **화면 설명** | 전체 주문 목록 조회 화면 |
| **주요 기능** | 주문 목록 조회, 주문번호별 그룹화, 필터링/검색 |
| **담당자** | 담당자 5 |
| **필요 DB 테이블** | `purchase_item`, `user`, `product`, `branch` |
| **필요 컬럼** | `purchase_item`: `b_seq`, `b_tnum`, `b_date`, `b_price`, `b_quantity`, `u_seq`, `p_seq`, `br_seq`<br>`user`: `u_seq`, `u_name`, `u_phone`<br>`product`: `p_seq`, `p_name`, `p_image`<br>`branch`: `br_seq`, `br_name` |
| **개발 API** | `GET /api/purchase_items`<br>`GET /api/purchase_items/by_tnum/{b_tnum}/with_details`<br>`GET /api/purchase_items/by_user/{user_seq}/orders` |

---

### 5. 관리자-주문목록 조회(상세화면)

| 항목 | 내용 |
|------|------|
| **화면 설명** | 특정 주문의 상세 정보 화면 (관리자가 수령 처리) |
| **주요 기능** | 주문 상세 정보 조회, 수령 완료 처리 |
| **담당자** | 담당자 5 |
| **필요 DB 테이블** | `purchase_item`, `user`, `product`, `branch`, `pickup`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` |
| **필요 컬럼** | `purchase_item`: 전체 컬럼<br>`user`: `u_seq`, `u_name`, `u_phone`<br>`product`: 전체 컬럼 + 카테고리 정보<br>`branch`: `br_seq`, `br_name`, `br_address`, `br_phone`<br>`pickup`: `pic_seq`, `pic_date`<br>카테고리 테이블: `kc_name`, `cc_name`, `sc_name`, `gc_name`<br>`maker`: `m_name` |
| **개발 API** | `GET /api/purchase_items/{b_seq}/full_detail`<br>`GET /api/purchase_items/by_tnum/{b_tnum}/with_details`<br>`GET /api/pickups/by_purchase/{b_seq}`<br>`POST /api/pickups/{pic_seq}/complete` |

---

### 6. 관리자-반품목록 조회

| 항목 | 내용 |
|------|------|
| **화면 설명** | 전체 반품 목록 조회 화면 |
| **주요 기능** | 반품 목록 조회, 필터링/검색 |
| **담당자** | 담당자 4 |
| **필요 DB 테이블** | `refund`, `user`, `staff`, `pickup`, `purchase_item`, `product` |
| **필요 컬럼** | `refund`: `ref_seq`, `ref_date`, `ref_reason`, `u_seq`, `s_seq`, `pic_seq`<br>`user`: `u_seq`, `u_name`, `u_phone`<br>`staff`: `s_seq`, `s_rank`<br>`product`: `p_seq`, `p_name`, `p_image` |
| **개발 API** | `GET /api/refunds`<br>`GET /api/refunds/by_staff/{staff_seq}/with_details` |

---

### 7. 관리자-반품목록 조회(상세화면)

| 항목 | 내용 |
|------|------|
| **화면 설명** | 특정 반품의 상세 정보 화면 (관리자가 반품 처리) |
| **주요 기능** | 반품 상세 정보 조회, 반품 승인/거부 처리 |
| **담당자** | 담당자 5 |
| **필요 DB 테이블** | `refund`, `user`, `staff`, `pickup`, `purchase_item`, `product`, `branch`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` |
| **필요 컬럼** | `refund`: 전체 컬럼<br>`user`: `u_seq`, `u_name`, `u_phone`<br>`staff`: `s_seq`, `s_rank`, `s_phone`<br>`pickup`: `pic_seq`, `pic_date`<br>`purchase_item`: 전체 컬럼<br>`product`: 전체 컬럼 + 카테고리 정보<br>`branch`: `br_seq`, `br_name`, `br_address` |
| **개발 API** | `GET /api/refunds/{refund_seq}/full_detail`<br>`POST /api/refunds/{refund_seq}/process` |

---

## 사용자 화면

### 8. 사용자 로그인

| 항목 | 내용 |
|------|------|
| **화면 설명** | 고객 로그인 화면 |
| **주요 기능** | ID/PW로 로그인 인증 |
| **담당자** | 담당자 1 |
| **필요 DB 테이블** | `user` |
| **필요 컬럼** | `u_id`, `u_password` |
| **개발 API** | `POST /api/users/login` |
| **참고** | 관리자 로그인과 비슷한 로직 (ID/PW 확인만)

---

### 9. 사용자 메뉴 드로어

| 항목 | 내용 |
|------|------|
| **화면 설명** | 사용자 메뉴 네비게이션 |
| **주요 기능** | 현재 로그인한 고객 정보 표시 |
| **담당자** | 담당자 1 |
| **필요 DB 테이블** | `user` |
| **필요 컬럼** | `u_seq`, `u_id`, `u_name`, `u_phone`, `u_image` |
| **개발 API** | `GET /api/users/{user_seq}`, `GET /api/users/{user_seq}/profile_image` |

---

### 10. 사용자-회원가입

| 항목 | 내용 |
|------|------|
| **화면 설명** | 고객 회원가입 화면 |
| **주요 기능** | 고객 정보 등록, 프로필 이미지 업로드 |
| **담당자** | 담당자 1 |
| **필요 DB 테이블** | `user` |
| **필요 컬럼** | `u_id`, `u_password`, `u_name`, `u_phone`, `u_image` |
| **개발 API** | `POST /api/users` |

---

### 11. 사용자-개인정보 수정

| 항목 | 내용 |
|------|------|
| **화면 설명** | 고객 개인정보 수정 화면 |
| **주요 기능** | 고객 정보 조회/수정, 프로필 이미지 관리 |
| **담당자** | 담당자 1 |
| **필요 DB 테이블** | `user` |
| **필요 컬럼** | `u_seq`, `u_id`, `u_password`, `u_name`, `u_phone`, `u_image` |
| **개발 API** | `GET /api/users/{user_seq}`, `GET /api/users/{user_seq}/profile_image`<br>`POST /api/users/{user_seq}`, `POST /api/users/{user_seq}/with_image`<br>`DELETE /api/users/{user_seq}/profile_image` |

---

### 12. 사용자-상품조회

| 항목 | 내용 |
|------|------|
| **화면 설명** | 상품 목록 조회 화면 (필터링 가능) |
| **주요 기능** | 상품 목록 조회, 카테고리별 필터링, 제조사별 조회 |
| **담당자** | 담당자 2 |
| **필요 DB 테이블** | `product`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` |
| **필요 컬럼** | `product`: `p_seq`, `p_name`, `p_price`, `p_stock`, `p_image`, `kc_seq`, `cc_seq`, `sc_seq`, `gc_seq`, `m_seq`<br>카테고리 테이블: `kc_name`, `cc_name`, `sc_name`, `gc_name`<br>`maker`: `m_name` |
| **개발 API** | `GET /api/products/with_categories`<br>`GET /api/products/by_category`<br>`GET /api/products/by_maker/{maker_seq}/with_categories`<br>`GET /api/makers`<br>`GET /api/kind_categories`, `GET /api/color_categories`, `GET /api/size_categories`, `GET /api/gender_categories` |
| **참고** | 상품 조회와 상세 화면은 연관성이 높아 한 명이 담당

---

### 13. 상품상세화면

| 항목 | 내용 |
|------|------|
| **화면 설명** | 특정 상품의 상세 정보 화면 |
| **주요 기능** | 상품 상세 정보 조회 (모든 카테고리 + 제조사 정보 포함) |
| **담당자** | 담당자 2 |
| **필요 DB 테이블** | `product`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` |
| **필요 컬럼** | `product`: 전체 컬럼<br>카테고리 테이블: `kc_name`, `cc_name`, `sc_name`, `gc_name`<br>`maker`: `m_seq`, `m_name`, `m_phone`, `m_address` |
| **개발 API** | `GET /api/products/{p_seq}/full_detail` |
| **참고** | 3D 프리뷰 기능은 담당자 6이 개발 (상품 상세 화면에 통합)

---

### 14. 사용자-장바구니

| 항목 | 내용 |
|------|------|
| **화면 설명** | 장바구니 화면 |
| **주요 기능** | 장바구니 조회, 상품 추가/수정/삭제 |
| **담당자** | 담당자 3 |
| **필요 DB 테이블** | `product` (장바구니는 DB 테이블 없이 임시 저장만 사용) |
| **필요 컬럼** | `product`: `p_seq`, `p_name`, `p_price`, `p_image`, `p_stock` |
| **개발 API** | 장바구니는 클라이언트에서 임시 저장 (메모리/로컬스토리지)<br>`GET /api/products/{p_seq}` - 상품 정보 조회<br>`GET /api/products/{p_seq}/stock` - 재고 확인 (장바구니 추가 시 필수)<br>`GET /api/products/check_stocks` - 여러 상품 재고 일괄 확인 (결제 전 확인)<br>결제 시 `POST /api/purchase_items`로 주문 생성 |
| **참고** | 장바구니는 DB 테이블 없이 임시 저장만 사용하지만, 상품 정보 조회 및 재고 확인을 위해 `product` 테이블 참조 필요

---

### 15. 사용자-주소:결제방법

| 항목 | 내용 |
|------|------|
| **화면 설명** | 주소 및 결제 방법 선택 화면 |
| **주요 기능** | 지점 선택 (픽업 지점), 고객 정보 확인 |
| **담당자** | 담당자 3 |
| **필요 DB 테이블** | `branch`, `user` |
| **필요 컬럼** | `branch`: `br_seq`, `br_name`, `br_address`, `br_phone`, `br_lat`, `br_lng`<br>`user`: `u_seq`, `u_name`, `u_phone` |
| **개발 API** | `GET /api/branches`<br>`GET /api/users/{user_seq}` |

---

### 16. 사용자-결제팝업

| 항목 | 내용 |
|------|------|
| **화면 설명** | 결제 팝업 화면 |
| **주요 기능** | 결제 금액 확인, 지점 정보 확인 |
| **담당자** | 담당자 3 |
| **필요 DB 테이블** | `product`, `branch` |
| **필요 컬럼** | `product`: `p_seq`, `p_name`, `p_price`, `p_stock`<br>`branch`: `br_seq`, `br_name` |
| **개발 API** | `GET /api/products/{p_seq}` - 상품 정보 조회<br>`GET /api/products/{p_seq}/stock` - 재고 확인<br>`GET /api/products/check_stocks` - 여러 상품 재고 일괄 확인<br>`GET /api/branches/{br_seq}` |
| **참고** | 결제 전 재고 확인 필수

---

### 17. 사용자-결제하기

| 항목 | 내용 |
|------|------|
| **화면 설명** | 결제 처리 화면 |
| **주요 기능** | 주문 생성, 수령 정보 생성, 재고 차감 |
| **담당자** | 담당자 3 |
| **필요 DB 테이블** | `purchase_item`, `pickup`, `product` |
| **필요 컬럼** | `purchase_item`: `br_seq`, `u_seq`, `p_seq`, `b_price`, `b_quantity`, `b_date`, `b_tnum`<br>`pickup`: `b_seq`, `pic_date`<br>`product`: `p_seq`, `p_stock` |
| **개발 API** | `GET /api/products/check_stocks` - 결제 전 재고 확인<br>`POST /api/purchase_items` - 주문 생성<br>`POST /api/pickups` - 수령 정보 생성<br>`PUT /api/products/{p_seq}/stock` - 재고 차감 (주문 생성 시 트랜잭션으로 처리) |
| **참고** | 재고 확인 후 주문 생성, 재고 차감은 트랜잭션으로 처리하여 동시성 문제 방지

---

### 18. 사용자- 주문내역 조회

| 항목 | 내용 |
|------|------|
| **화면 설명** | 고객의 주문 내역 목록 화면 |
| **주요 기능** | 고객별 주문 목록 조회 (주문번호별 그룹화) |
| **담당자** | 담당자 4 |
| **필요 DB 테이블** | `purchase_item`, `product`, `branch` |
| **필요 컬럼** | `purchase_item`: `b_seq`, `b_tnum`, `b_date`, `b_price`, `b_quantity`, `p_seq`, `br_seq`<br>`product`: `p_seq`, `p_name`, `p_price`, `p_image`<br>`branch`: `br_seq`, `br_name` |
| **개발 API** | `GET /api/purchase_items/by_user/{user_seq}/orders`<br>`GET /api/purchase_items/by_user/{user_seq}/with_details` |

---

### 19. 사용자- 주문내역 조회(상세화면)

| 항목 | 내용 |
|------|------|
| **화면 설명** | 특정 주문의 상세 정보 화면 |
| **주요 기능** | 주문 상세 정보 조회, 수령 정보 확인 |
| **담당자** | 담당자 4 |
| **필요 DB 테이블** | `purchase_item`, `user`, `product`, `branch`, `pickup`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` |
| **필요 컬럼** | `purchase_item`: 전체 컬럼<br>`user`: `u_seq`, `u_name`, `u_phone`<br>`product`: 전체 컬럼 + 카테고리 정보<br>`branch`: `br_seq`, `br_name`, `br_address`<br>`pickup`: `pic_seq`, `pic_date` |
| **개발 API** | `GET /api/purchase_items/by_tnum/{b_tnum}/with_details`<br>`GET /api/purchase_items/{b_seq}/full_detail`<br>`GET /api/pickups/by_purchase/{b_seq}` |

---

### 20. 사용자-수령 반품목록 조회

| 항목 | 내용 |
|------|------|
| **화면 설명** | 고객의 수령 및 반품 목록 화면 (조회만 가능) |
| **주요 기능** | 수령 내역 조회, 반품 내역 조회 |
| **담당자** | 담당자 4 |
| **필요 DB 테이블** | `pickup`, `purchase_item`, `product`, `branch`, `refund`, `staff` |
| **필요 컬럼** | `pickup`: `pic_seq`, `pic_date`, `b_seq`<br>`purchase_item`: `b_seq`, `b_price`, `b_quantity`, `b_date`, `p_seq`<br>`product`: `p_seq`, `p_name`, `p_image`<br>`branch`: `br_seq`, `br_name`<br>`refund`: `ref_seq`, `ref_date`, `ref_reason`<br>`staff`: `s_seq`, `s_rank` |
| **개발 API** | `GET /api/pickups/by_user/{user_seq}/with_details`<br>`GET /api/refunds/by_user/{user_seq}/with_details` |

---

### 21. 사용자-수령 반품목록 조회(상세화면)

| 항목 | 내용 |
|------|------|
| **화면 설명** | 특정 수령/반품의 상세 정보 화면 (조회만 가능) |
| **주요 기능** | 수령 상세 정보 조회, 반품 상세 정보 조회, 반품 신청 |
| **담당자** | 담당자 4 |
| **필요 DB 테이블** | `pickup`, `purchase_item`, `product`, `branch`, `refund`, `staff`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` |
| **필요 컬럼** | `pickup`: 전체 컬럼<br>`purchase_item`: 전체 컬럼<br>`product`: 전체 컬럼 + 카테고리 정보<br>`branch`: `br_seq`, `br_name`, `br_address`, `br_phone`<br>`refund`: 전체 컬럼<br>`staff`: `s_seq`, `s_rank`, `s_phone` |
| **개발 API** | `GET /api/pickups/{pic_seq}/full_detail`<br>`GET /api/refunds/{refund_seq}/full_detail`<br>`POST /api/refunds` |

---

## DB 테이블 구조 요약

### 주요 테이블

| 테이블명 | 설명 | 주요 컬럼 |
|---------|------|----------|
| `branch` | 오프라인 지점 정보 | `br_seq`, `br_name`, `br_address`, `br_phone`, `br_lat`, `br_lng` |
| `user` | 고객 계정 | `u_seq`, `u_id`, `u_password`, `u_name`, `u_phone`, `u_image` |
| `staff` | 직원 계정 | `s_seq`, `br_seq`, `s_password`, `s_rank`, `s_phone`, `s_image`, `s_superseq` |
| `maker` | 제조사 | `m_seq`, `m_name`, `m_phone`, `m_address` |
| `kind_category` | 종류 카테고리 | `kc_seq`, `kc_name` |
| `color_category` | 색상 카테고리 | `cc_seq`, `cc_name` |
| `size_category` | 사이즈 카테고리 | `sc_seq`, `sc_name` |
| `gender_category` | 성별 카테고리 | `gc_seq`, `gc_name` |
| `product` | 판매 상품(SKU) | `p_seq`, `kc_seq`, `cc_seq`, `sc_seq`, `gc_seq`, `m_seq`, `p_name`, `p_price`, `p_stock`, `p_image` |
| `purchase_item` | 구매 내역 | `b_seq`, `br_seq`, `u_seq`, `p_seq`, `b_price`, `b_quantity`, `b_date`, `b_tnum` |
| `pickup` | 오프라인 수령 | `pic_seq`, `b_seq`, `pic_date` |
| `refund` | 반품/환불 | `ref_seq`, `ref_date`, `ref_reason`, `u_seq`, `s_seq`, `pic_seq` |
| `receive` | 입고 | `rec_seq`, `p_seq`, `rec_quantity`, `rec_date`, `s_seq` |
| `request` | 발주 | `req_seq`, `p_seq`, `req_quantity`, `req_date`, `s_seq`, `req_status` |

### 테이블 관계

- `product` → `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` (FK)
- `purchase_item` → `branch`, `user`, `product` (FK)
- `pickup` → `purchase_item` (FK: `b_seq`)
- `refund` → `user`, `staff`, `pickup` (FK)
- `staff` → `branch` (FK: `br_seq`)

---

## 공통 개발 가이드

### 인증 방식
- 로그인: ID/PW 확인 방식 (단순 인증)
- 로그인 후 사용자 정보는 클라이언트에서 관리

### 수령/반품 처리
- 사용자: 수령/반품 신청만 가능
- 관리자: 수령/반품 승인 및 처리 담당

### 주문 그룹화
- `b_tnum` (결제 트랜잭션 번호)로 여러 주문 항목을 하나의 주문으로 그룹화
- 동일한 `b_tnum`을 가진 `purchase_item`들은 하나의 주문으로 처리

### 이미지 처리
- 프로필 이미지: `MEDIUMBLOB` 타입으로 저장
- 제품 이미지: `VARCHAR(255)` 경로 문자열로 저장

---

## 추가 작업 화면 (Firebase)

### 21. 관리자-공지 등록

| 항목 | 내용 |
|------|------|
| **화면 설명** | 공지사항 등록 화면 (Firebase 사용) |
| **주요 기능** | 공지사항 작성, 등록, 수정, 삭제 |
| **담당자** | 추가 작업 |
| **필요 DB 테이블** | Firebase Firestore (MySQL 테이블 불필요) |
| **필요 컬럼** | Firebase Firestore 컬렉션: `notices`<br>필드: `title`, `content`, `created_at`, `updated_at`, `author`, `is_active` |
| **개발 API** | Firebase SDK 사용<br>`POST /api/firebase/notices` (Firebase Admin SDK)<br>`PUT /api/firebase/notices/{notice_id}`<br>`DELETE /api/firebase/notices/{notice_id}` |
| **참고** | Firebase Firestore를 사용하여 공지사항 관리, 실시간 업데이트 지원 가능

---

### 22. 사용자-공지 조회

| 항목 | 내용 |
|------|------|
| **화면 설명** | 공지사항 조회 화면 (Firebase 사용) |
| **주요 기능** | 공지사항 목록 조회, 상세 조회 |
| **담당자** | 추가 작업 |
| **필요 DB 테이블** | Firebase Firestore (MySQL 테이블 불필요) |
| **필요 컬럼** | Firebase Firestore 컬렉션: `notices`<br>필드: `title`, `content`, `created_at`, `author`, `is_active` |
| **개발 API** | Firebase SDK 사용<br>`GET /api/firebase/notices`<br>`GET /api/firebase/notices/{notice_id}` |
| **참고** | Firebase Firestore를 사용하여 공지사항 조회, 실시간 업데이트 지원 가능

---

### 23. 관리자-상담 채팅

| 항목 | 내용 |
|------|------|
| **화면 설명** | 고객 상담 채팅 화면 (Firebase 사용) |
| **주요 기능** | 채팅방 목록 조회, 채팅 메시지 송수신, 채팅방 관리 |
| **담당자** | 추가 작업 |
| **필요 DB 테이블** | Firebase Firestore (MySQL 테이블 불필요) |
| **필요 컬럼** | Firebase Firestore 컬렉션: `chat_rooms`, `messages`<br>`chat_rooms`: `room_id`, `user_id`, `staff_id`, `created_at`, `last_message`, `status`<br>`messages`: `message_id`, `room_id`, `sender_id`, `sender_type`, `content`, `timestamp`, `read` |
| **개발 API** | Firebase SDK 사용<br>`GET /api/firebase/chat_rooms`<br>`GET /api/firebase/chat_rooms/{room_id}/messages`<br>`POST /api/firebase/chat_rooms/{room_id}/messages`<br>`PUT /api/firebase/messages/{message_id}/read` |
| **참고** | Firebase Firestore를 사용하여 실시간 채팅 구현, 푸시 알림 연동 가능

---

### 24. 사용자-상담 채팅

| 항목 | 내용 |
|------|------|
| **화면 설명** | 고객 상담 채팅 화면 (Firebase 사용) |
| **주요 기능** | 채팅방 생성, 채팅 메시지 송수신, 채팅 이력 조회 |
| **담당자** | 추가 작업 |
| **필요 DB 테이블** | Firebase Firestore (MySQL 테이블 불필요) |
| **필요 컬럼** | Firebase Firestore 컬렉션: `chat_rooms`, `messages`<br>`chat_rooms`: `room_id`, `user_id`, `staff_id`, `created_at`, `last_message`, `status`<br>`messages`: `message_id`, `room_id`, `sender_id`, `sender_type`, `content`, `timestamp`, `read` |
| **개발 API** | Firebase SDK 사용<br>`POST /api/firebase/chat_rooms`<br>`GET /api/firebase/chat_rooms/{room_id}/messages`<br>`POST /api/firebase/chat_rooms/{room_id}/messages`<br>`PUT /api/firebase/messages/{message_id}/read` |
| **참고** | Firebase Firestore를 사용하여 실시간 채팅 구현, 푸시 알림 연동 가능

---

## 참고사항

1. **API 개발**: FastAPI 기반으로 개발하며, 화면 요구사항에 맞춰 API 엔드포인트를 설계합니다.
2. **DB 스키마**: `backend/database/renew/shoes_shop_db_mysql_init_improved.sql` 파일 참조
3. **작업 협의**: 공통 응답 형식, 에러 처리 방식 등은 담당자 간 협의가 필요합니다.
4. **수주/발주 관리**: `request`, `receive` 테이블은 차후 화면 개발 시 활용 가능합니다.
5. **Firebase 기능**: 공지사항과 상담 채팅은 Firebase Firestore를 사용하며, MySQL 테이블이 필요하지 않습니다.

---

**참고**: 최소 버전은 `SCREEN_API_MAPPING_SUMMARY.md` 파일 참조

