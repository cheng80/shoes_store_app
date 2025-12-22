# 진행 상황 (Progress)

## 📅 최종 업데이트: 2025-12-17 (Retail 테이블 제거 완료)

---

## ✅ 완료된 기능

### 1. 인증 및 사용자 관리

#### 사용자 (Customer) 기능
- ✅ **로그인 화면** (`login_screen.dart`)
  - 이메일 또는 전화번호로 로그인 가능
  - `CustomCommonUtil.isEmail()`을 사용한 정교한 이메일 검증
  - 로그인 성공 시 `UserStorage`에 사용자 정보 저장
  - 로고 5번 연속 탭으로 관리자 진입 모드 (태블릿/모바일 자동 감지)
  
- ✅ **회원가입 화면** (`signup_screen.dart`)
  - 이메일 기반 회원가입
  - 이메일 중복 검사
  - 비밀번호 확인 검증
  - 회원가입 성공 시 `Customer` DB에 저장
  - 테스트용 더미 데이터 지원

- ✅ **사용자 프로필 수정** (`user_profile_edit.dart`)
  - 이메일은 읽기 전용
  - 이름, 전화번호, 비밀번호 수정 가능
  - 비밀번호는 선택적 수정 (비워두면 기존 비밀번호 유지)
  - 수정 성공 시 DB 및 `UserStorage` 업데이트

#### 관리자 (Employee) 기능
- ✅ **관리자 로그인 화면** (`admin_login.dart`)
  - 태블릿 전용 (가로 모드 강제)
  - 모바일 접근 시 차단 화면으로 리다이렉트
  - 이메일 또는 전화번호로 로그인
  - 로그인 성공 시 `AdminStorage`에 관리자 정보 저장
  - 회원가입 기능 없음 (로그인만 가능)

- ✅ **관리자 프로필 수정** (`admin_profile_edit.dart`)
  - 이메일은 읽기 전용
  - 이름, 전화번호, 비밀번호 수정 가능
  - 비밀번호는 선택적 수정
  - 수정 성공 시 DB 및 `AdminStorage` 업데이트
  - 수정 후 이전 페이지로 자동 이동 및 드로워 정보 갱신

- ✅ **모바일 접근 차단 화면** (`admin_mobile_block_screen.dart`)
  - 관리자 기능은 태블릿에서만 사용 가능 안내

### 2. 관리자 주문 관리

- ✅ **주문 관리 화면** (`admin_employee_order_view.dart`)
  - 주문 목록 표시 (좌측)
  - 주문 상세 정보 표시 (우측)
  - 주문자 정보 카드 (`CustomerInfoCard`)
  - 주문 상품 목록 및 총 가격 표시
  - 픽업 완료 버튼
  - 관리자 드로워 메뉴 통합

- ✅ **반품 관리 화면** (`admin_employee_return_order_view.dart`)
  - 반품 주문 목록 표시
  - 반품 상세 정보 표시
  - 반품 확인 버튼
  - 관리자 드로워 메뉴 통합

### 3. 공통 컴포넌트

#### 관리자/직원 관련 (`employee_sub_dir/`)
- ✅ **관리자 드로워** (`admin_drawer.dart`)
  - 주문 관리, 반품 관리 메뉴
  - 프로필 수정 메뉴
  - 관리자 이름 및 역할 표시 (`AdminStorage`에서 로드)

- ✅ **태블릿 유틸리티** (`admin_tablet_utils.dart`)
  - 태블릿 감지 (`isTablet()`)
  - 가로 모드 고정 (`lockTabletLandscape()`)
  - 방향 잠금 해제 (`unlockAllOrientations()`)
  - iOS 기기 (iPad Mini 등) 지원을 위한 최적화된 감지 로직

- ✅ **관리자 저장소** (`admin_storage.dart`)
  - `get_storage`를 사용한 관리자 정보 저장/불러오기
  - 관리자 이름, 이메일, 전화번호, 역할 관리

- ✅ **주문 카드 컴포넌트**
  - `BaseOrderCard`: 주문 카드 기본 클래스
  - `OrderCard`: 주문 관리용 카드
  - `ReturnOrderCard`: 반품 관리용 카드
  - `OrderDetailView`: 주문 상세 정보 뷰
  - `ReturnOrderDetailView`: 반품 상세 정보 뷰
  - `OrderUtils`: 주문 관련 유틸리티 (가격 포맷팅 등)

#### 고객 관련 (`customer_sub_dir/`)
- ✅ **고객 정보 카드** (`customer_info_card.dart`)
  - 주문자 상세 정보 표시 (이름, 연락처, 이메일)
  - 주문 관리 및 반품 관리 화면에서 공통 사용

- ✅ **사용자 저장소** (`user_storage.dart`)
  - `get_storage`를 사용한 사용자 정보 저장/불러오기
  - 사용자 이름, 이메일, 전화번호 관리

### 4. 데이터베이스 및 저장소

- ✅ **DB 초기화 중앙화**
  - `main.dart`에서 단일 호출로 DB 초기화 및 더미 데이터 삽입
  - 각 화면에서 중복 호출 제거
  - GetStorage로 초기화 완료 여부 저장하여 앱 재실행 시 중복 초기화 방지
  - `DatabaseManager.closeAndReset()` 메서드 추가로 DB 연결 안전하게 닫기

- ✅ **데이터 모델**
  - `Customer` 모델: 필드명 변경 (`cPname` → `cName`)
  - `Employee` 모델: 관리자 정보 관리

- ✅ **로컬 저장소**
  - `get_storage` 초기화 (`main.dart`)
  - `UserStorage`: 사용자 정보 관리
  - `AdminStorage`: 관리자 정보 관리
  - DB 초기화 상태 저장 (`kStorageKeyDBInitialized`)

### 5. 폴더 구조 정리

- ✅ **폴더 구조 개선**
  - `administer_emplyee/` → `employee_sub_dir/` (관리자/직원 관련)
  - `customer/` → `customer_sub_dir/` (고객 관련)
  - Employee와 Customer 관련 클래스 분리

### 6. 테스트 및 디버깅

- ✅ **테스트 네비게이션 페이지** (`test_navigation_page.dart`)
  - 모든 화면으로의 네비게이션 테스트
  - DB 조회 테스트 (모든 사용자 출력)
  - 회원가입 더미 데이터 테스트
  - DB 초기화 및 더미 데이터 재삽입 버튼 추가 (수동 초기화 기능)

---

## 🔧 기술적 개선 사항

1. **코드 중복 제거**
   - 태블릿 유틸리티 함수 통합
   - 주문 카드 베이스 클래스로 공통 로직 추출
   - 하드코딩된 값들을 `config.dart`로 중앙화

2. **상태 관리**
   - `get_storage`를 사용한 세션 관리
   - 프로필 수정 후 자동 UI 갱신 (`setState` 활용)
   - DB 초기화 상태 관리 (중복 초기화 방지)

3. **에러 처리**
   - 로그인/회원가입 실패 시 명확한 피드백
   - DB 조회 에러 처리
   - DB 연결 안전하게 닫기 (`closeAndReset()`)

4. **사용자 경험**
   - 로딩 인디케이터 추가
   - 성공/실패 스낵바 메시지
   - 확인 다이얼로그 (프로필 수정 시, DB 초기화 시)

5. **플랫폼 최적화**
   - iOS 기기 태블릿 감지 개선 (iPad Mini 지원)
   - 태블릿 가로 모드 강제

6. **코드 품질 개선**
   - 하드코딩 제거: `pickupStatus`, `loginStatus`, `district` 관련 하드코딩을 `config.dart` 값으로 대체
   - 주석 추가: config 값 사용 부분에 실제 데이터 값 주석 추가로 가독성 향상

---

## 📝 참고 사항

- 모든 화면은 `custom` 폴더의 커스텀 위젯을 사용
- DB 초기화는 `main.dart`에서만 수행 (GetStorage로 중복 초기화 방지)
- 사용자/관리자 정보는 `get_storage`에 저장되어 앱 재시작 후에도 유지 가능
- 관리자 기능은 태블릿에서만 사용 가능 (보안상의 이유)
- 모든 상태값(`pickupStatus`, `loginStatus`, `district`)은 `config.dart`에서 중앙 관리
- 테스트 페이지에서 수동으로 DB를 재초기화할 수 있음

---

## ✅ 최근 완료된 작업

### 2025-12-17

#### 1. 주문 상세 뷰 버튼 상태 표시 개선
- **파일**: `lib/view/cheng/screens/customer/order_detail_view.dart`
- **내용**: 하단 버튼 텍스트가 현재 주문 상태에 맞게 동적으로 표시되도록 개선
  - "제품 준비 중" 상태: 버튼도 "제품 준비 중"으로 표시 (비활성화)
  - "제품 준비 완료" 상태: 버튼은 "픽업 완료"로 표시 (활성화)
  - "제품 수령 완료" 상태: 버튼은 "제품 수령 완료"로 표시 (비활성화)

#### 2. 결제 시 Purchase 객체 생성 로직 추가
- **파일**: `lib/view/customer/purchase_view.dart`
- **내용**: 
  - 결제 시 `Purchase` 객체를 자동으로 생성하도록 수정
  - `timeStamp`: 현재 날짜/시간 (`DateTime.now().toIso8601String()`)
  - `pickupDate`: 현재 날짜 + 1일 (`DateTime.now().add(Duration(days: 1))`)
  - `orderCode`: `OrderUtils.generateOrderCode(userId)` 사용
  - 생성된 `Purchase` ID를 `PurchaseItem`의 `pcid`로 연결
  - 현재 로그인한 사용자 ID는 `UserStorage.getUserId()`로 가져옴

#### 3. 주문 상태 결정 로직 개선
- **파일**: `lib/utils/order_status_utils.dart`
- **내용**: 
  - `isPickupDatePassed` 함수 추가: `pickupDate`가 오늘보다 작거나 같을 때도 "제품 준비 완료" 상태로 처리
  - 기존 `isPickupDateToday`는 오늘과 같을 때만 처리했으나, 이제 `pickupDate <= 오늘`인 경우 모두 처리
  - `determineOrderStatusForCustomer`와 `determineOrderStatusForAdmin`에 적용
  - 예시: 12월 15일 결제 → `pickupDate = 12월 16일` → 12월 17일 확인 시 "제품 준비 완료"로 정상 표시

### 2025-12-17 (추가)

#### 4. 하드코딩 제거 및 Config 중앙화
- **파일**: 전체 프로젝트
- **내용**:
  - `pickupStatus` 관련 하드코딩 제거: 더미 데이터, fallback 값, UI 표시용 값들을 `config.pickupStatus`로 대체
  - `loginStatus` 관련 하드코딩 제거: `login_view.dart`의 하드코딩된 값들을 `config.loginStatus`로 대체
  - `district` 관련 하드코딩 제거: 더미 데이터의 하드코딩된 지역명을 `config.district`로 대체
  - 주석 추가: 모든 config 값 사용 부분에 실제 데이터 값 주석 추가 (예: `config.pickupStatus[1] // '제품 준비 완료'`)
  - 수정된 파일: `dummy_data_constants.dart`, `dummy_data_sets.dart`, `order_status_utils.dart`, `purchase_service.dart`, `login_view.dart` 등 총 10개 파일

#### 5. DB 초기화 로직 개선
- **파일**: `lib/main.dart`, `lib/database/core/database_manager.dart`, `lib/view/cheng/test_navigation_page.dart`
- **내용**:
  - GetStorage로 DB 초기화 완료 여부 저장 (`kStorageKeyDBInitialized`)
  - 앱 재실행 시 이미 초기화된 경우 중복 초기화 방지
  - `DatabaseManager.closeAndReset()` 메서드 추가: DB 연결을 안전하게 닫고 인스턴스 리셋
  - 테스트 페이지에 "DB 초기화 및 더미 데이터 재삽입" 버튼 추가: 수동으로 DB를 재초기화할 수 있는 기능
  - DB 삭제 전 기존 연결 닫기로 `database_closed` 에러 해결

### 2025-12-17 (문서 정리 및 구조화)

#### 6. 프로젝트 문서 정리 및 구조화
- **파일**: `specs/` 폴더 전체
- **내용**:
  - 마이그레이션 완료 문서 삭제: `DATABASE_MIGRATION_PLAN.md`, `REFACTORING_COMPLETION_STATUS.md`, `CHENG_FOLDER_REFACTORING_PLAN.md`, `INTEGRATED_REFACTORING_PLAN.md`, `DUMMY_DATA_REFACTORING_PLAN.md`, `PROJECT_RENAME_GUIDE.md` (총 6개)
  - `DATABASE_GUIDE.md` 생성: 데이터베이스 관련 핵심 정보 통합 가이드 (스키마, 핸들러 사용법, 쿼리 작성 가이드 통합)
  - `SCREEN_PROCESSING_PATTERNS.md` 재작성: 효율적이고 단순한 화면 로직 처리 패턴 중심으로 재구성
  - `PURCHASE_LIST_ANALYSIS.md` 삭제: 현재 로직과 맞지 않아 삭제
  - `README.md` 업데이트: 카테고리별 문서 구조 정리 및 각 문서의 역할 명시

#### 7. 문서 가이드 개선
- **파일**: `specs/README.md`, `specs/TODO.md`, `specs/PROGRESS.md`
- **내용**:
  - `TODO.md`와 `PROGRESS.md`의 역할 명확화: 작업 계획 vs 완료 기록
  - 문서 사용 가이드 추가: 두 문서의 차이점과 사용 방법 명시
  - 카테고리별 문서 구조 정리: 프로젝트 관리, 데이터베이스, 개발 가이드, 참고 자료로 분류

#### 8. 주문 상태 로직 문서 검토 및 업데이트
- **파일**: `specs/ORDER_STATUS_LOGIC_IMPROVEMENT.md`
- **내용**:
  - 실제 구현 상태와 문서 일치 여부 검토
  - 구현 완료된 항목 정리 및 문서 업데이트
  - 함수 목록 보완: 실제 구현된 함수 목록으로 업데이트
  - 구현 상태 검토 섹션 추가: 완료된 항목 및 문서 업데이트 필요 사항 명시

#### 9. Retail 테이블 및 관련 코드 제거
- **파일**: 
  - `lib/model/sale/retail.dart` (삭제)
  - `lib/database/handlers/retail_handler.dart` (삭제)
  - `lib/database/core/database_manager.dart`
  - `lib/config.dart`
  - `specs/DATABASE_SCHEMA.md`
  - `specs/DATABASE_GUIDE.md`
  - `specs/HANDLER_USAGE_GUIDE.md`
  - `specs/TODO.md`
- **내용**:
  - **배경**: 현재 로직에서는 `Product.pQuantity`로 본사가 재고를 중앙 관리하므로 Retail 테이블이 사용되지 않음
  - **제거된 파일**:
    - Retail 모델 파일 삭제
    - RetailHandler 파일 삭제
  - **코드 수정**:
    - `DatabaseManager`: Retail 테이블 생성 및 인덱스 생성 로직 제거
    - `DatabaseManager.clearAllTables()`: Retail 테이블 삭제 로직 제거
    - `config.dart`: `kTableRetail` 상수 제거, 업데이트 로그 정리
  - **문서 업데이트**:
    - `DATABASE_SCHEMA.md`: Retail 테이블 관련 내용 제거, 재고 관리 방식 명시
    - `DATABASE_GUIDE.md`: Retail 테이블 제거, 재고 관리 방식 명시
    - `HANDLER_USAGE_GUIDE.md`: RetailHandler 제거, 미사용 상태 명시
    - `TODO.md`: 인덱스 목록에서 Retail 제거, 재고 관리 방식 명시
  - **결과**: 대리점별 재고 관리 기능은 미구현이며, 모든 재고는 본사가 `Product.pQuantity`로 중앙 관리

## 🎯 다음 단계

작업 계획 및 할 일 목록은 `TODO.md`를 참고하세요.

---

## 📝 문서 사용 가이드

### 이 문서의 목적
- **완료된 작업의 상세 기록**: 구현 내용, 변경 사항, 기술적 개선 사항
- **작업 이력 관리**: 날짜별 완료된 작업 추적
- **기술 문서**: 향후 유사한 작업 시 참고 자료

### TODO.md와의 관계
- **TODO.md**: 작업 계획 및 진행 상황 (체크박스로 완료 표시)
- **PROGRESS.md**: 완료된 작업의 상세 기록 (이 문서)
- 두 문서는 서로 보완적 관계입니다.
  - TODO.md에서 작업 완료 체크 → 간단한 완료 표시
  - PROGRESS.md에 상세 내용 기록 → 완료된 작업의 이력 관리

