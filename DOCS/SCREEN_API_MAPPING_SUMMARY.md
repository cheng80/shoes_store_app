# 화면별 개발 가이드 - 최소 버전

**작성일**: 2025-01-XX  
**목적**: 화면 개발 시 필요한 DB 테이블 및 담당자 정보

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

**총 화면 수:** 20개 (기본 화면)  
**추가 작업 화면:** 4개 (Firebase 공지 2개, Firebase 상담 채팅 2개)  
**평균 화면 수:** 4.0개/인 (담당자 6 제외)

**참고**: 
- 주문/반품 조회는 사용자용과 관리자용이 거의 동일한 데이터 사용
- 담당자 4와 5는 협업하여 공통 API를 먼저 개발하고 필터링 조건만 추가하는 것을 권장
- 장바구니는 DB 테이블 없이 임시 저장(메모리/로컬스토리지)으로만 사용하지만, 상품 정보 조회 및 재고 확인을 위해 `product` 테이블 참조 필요

---

## 관리자 화면

| 화면 이름 | 화면 설명 | 필요 테이블명 | 담당자 |
|----------|----------|--------------|--------|
| 관리자-로그인 | 관리자(직원) 로그인 화면 | `staff` | 담당자 1 |
| 관리자-드로어 메뉴 | 관리자 메뉴 네비게이션 | `staff` | 담당자 1 |
| 관리자-개인정보 수정 | 관리자 개인정보 수정 화면 | `staff`, `branch` | 담당자 1 |
| 관리자-주문목록 조회 | 전체 주문 목록 조회 화면 | `purchase_item`, `user`, `product`, `branch` | 담당자 5 |
| 관리자-주문목록 조회(상세화면) | 특정 주문의 상세 정보 화면 (관리자가 수령 처리) | `purchase_item`, `user`, `product`, `branch`, `pickup`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` | 담당자 5 |
| 관리자-반품목록 조회 | 전체 반품 목록 조회 화면 | `refund`, `user`, `staff`, `pickup`, `purchase_item`, `product` | 담당자 5 |
| 관리자-반품목록 조회(상세화면) | 특정 반품의 상세 정보 화면 (관리자가 반품 처리) | `refund`, `user`, `staff`, `pickup`, `purchase_item`, `product`, `branch`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` | 담당자 5 |
| 관리자-공지 등록 | 공지사항 등록 화면 (Firebase) | Firebase Firestore | 추가 작업 |
| 관리자-상담 채팅 | 고객 상담 채팅 화면 (Firebase) | Firebase Firestore | 추가 작업 |

---

## 사용자 화면

| 화면 이름 | 화면 설명 | 필요 테이블명 | 담당자 |
|----------|----------|--------------|--------|
| 사용자 로그인 | 고객 로그인 화면 | `user` | 담당자 1 |
| 사용자 메뉴 드로어 | 사용자 메뉴 네비게이션 | `user` | 담당자 1 |
| 사용자-회원가입 | 고객 회원가입 화면 | `user` | 담당자 1 |
| 사용자-개인정보 수정 | 고객 개인정보 수정 화면 | `user` | 담당자 1 |
| 사용자-상품조회 | 상품 목록 조회 화면 (필터링 가능) | `product`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` | 담당자 2 |
| 상품상세화면 | 특정 상품의 상세 정보 화면 (3D 프리뷰 포함) | `product`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` | 담당자 2 (3D 프리뷰: 담당자 6) |
| 사용자-장바구니 | 장바구니 화면 | `product` (임시 저장, 재고 확인 필요) | 담당자 3 |
| 사용자-주소:결제방법 | 주소 및 결제 방법 선택 화면 | `branch`, `user` | 담당자 3 |
| 사용자-결제팝업 | 결제 팝업 화면 | `product`, `branch` | 담당자 3 |
| 사용자-결제하기 | 결제 처리 화면 | `purchase_item`, `pickup`, `product` | 담당자 3 |
| 사용자- 주문내역 조회 | 고객의 주문 내역 목록 화면 | `purchase_item`, `product`, `branch` | 담당자 4 |
| 사용자- 주문내역 조회(상세화면) | 특정 주문의 상세 정보 화면 | `purchase_item`, `user`, `product`, `branch`, `pickup`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` | 담당자 4 |
| 사용자-수령 반품목록 조회 | 고객의 수령 및 반품 목록 화면 (조회만 가능) | `pickup`, `purchase_item`, `product`, `branch`, `refund`, `staff` | 담당자 4 |
| 사용자-수령 반품목록 조회(상세화면) | 특정 수령/반품의 상세 정보 화면 (조회만 가능) | `pickup`, `purchase_item`, `product`, `branch`, `refund`, `staff`, `kind_category`, `color_category`, `size_category`, `gender_category`, `maker` | 담당자 4 |
| 사용자-공지 조회 | 공지사항 조회 화면 (Firebase) | Firebase Firestore | 추가 작업 |
| 사용자-상담 채팅 | 고객 상담 채팅 화면 (Firebase) | Firebase Firestore | 추가 작업 |

---

## DB 테이블 구조 요약

| 테이블명 | 설명 |
|---------|------|
| `branch` | 오프라인 지점 정보 |
| `user` | 고객 계정 |
| `staff` | 직원 계정 |
| `maker` | 제조사 |
| `kind_category` | 종류 카테고리 |
| `color_category` | 색상 카테고리 |
| `size_category` | 사이즈 카테고리 |
| `gender_category` | 성별 카테고리 |
| `product` | 판매 상품(SKU) |
| `purchase_item` | 구매 내역 |
| `pickup` | 오프라인 수령 |
| `refund` | 반품/환불 |
| `receive` | 입고 |
| `request` | 발주 |

**참고**: 
- Firebase 기능(공지, 상담 채팅)은 MySQL 테이블이 아닌 Firebase Firestore를 사용합니다.

---

