# 주문 상태 결정 로직 개선 계획

**작성일**: 2025-12-13  
**목적**: 주문 상태 결정 로직의 중복 제거 및 요구사항 반영

---

## 📋 현재 문제점

1. **중복 코드**: `_parseStatusToNumber`, `_determineOrderStatus`가 4개 파일에 중복 존재
2. **날짜 비교 로직 부재**:
   - timeStamp와 오늘 날짜 비교 없음 (구매 당일 체크)
   - pickupDate와 오늘 날짜 비교 없음 (자동 준비 완료 체크)
   - 30일 경과만 체크하고 있음
3. **로직 불일치**: 고객/관리자 화면 간 로직 차이 있음

---

## 🎯 요구사항 정리

### 1. 구매 당일 체크
- **조건**: `timeStamp`의 날짜 == 오늘 날짜
- **결과**: status 0 (제품 준비 중)

### 2. 자동 준비 완료
- **조건**: `pickupDate`의 날짜 <= 오늘 날짜
- **설명**: 하루가 지나면 자동으로 제품이 준비됨 (픽업 날짜가 되었거나 지났으면 준비 완료)
- **결과**: status 1 (제품 준비 완료)
- **개선 이력 (2025-12-17)**: `pickupDate == 오늘`에서 `pickupDate <= 오늘`로 변경하여 지난 날짜도 처리하도록 개선

### 3. 30일 경과 자동 수령 완료
- **조건**: `pickupDate`로부터 30일 이상 경과
- **결과**: status 2 (제품 수령 완료)

### 4. 상태 >= 2 표시 규칙
- **조건**: 최종 결정된 상태가 2 이상
- **결과**: 무조건 "제품 수령 완료" (status 2)로 표시

### 5. 픽업 완료 버튼
- **활성화 조건**: status 1 (제품 준비 완료)일 때만
- **동작**: 클릭 시 status 2 (제품 수령 완료)로 변경

---

## 🔧 개선 방향

### 1. 공용 유틸리티 클래스 생성

**파일**: `lib/view/cheng/utils/order_status_utils.dart`

**함수 목록**:
- `parseStatusToNumber(String pcStatus)`: pcStatus를 숫자로 변환 ✅
- `determineOrderStatusForCustomer(...)`: 주문 상태 결정 (고객 화면용) ✅
- `determineOrderStatusForAdmin(...)`: 주문 상태 결정 (관리자 화면용) ✅
- `shouldAutoUpdateToCompleted(...)`: 30일 경과 자동 수령 완료 여부 ✅
- `isPickupDatePassed30Days(...)`: 픽업 날짜로부터 30일 이상 경과 확인 ✅
- `isPurchaseDateToday(...)`: 구매 당일 확인 ✅
- `determineReturnStatus(...)`: 반품 가능 여부 결정 ✅

### 2. 상태 결정 로직 개선

**우선순위**:
1. 반품 상태(3 이상)가 있으면 그대로 반환 (반품 상태는 날짜 기반 자동 변경 불가)
2. 30일 경과 체크 → status 2
3. pickupDate 당일 체크 → status 1
4. timeStamp 당일 체크 → status 0
5. PurchaseItem의 pcStatus 기반 결정

**날짜 비교 방식**:
- 날짜 부분만 비교 (시간 제외)
- `DateTime.parse()` 후 날짜 부분만 추출하여 비교

### 3. 적용 범위

**고객 화면**:
- `order_list_view.dart`: 목록에서 상태 표시
- `order_detail_view.dart`: 상세 화면에서 상태 표시 및 버튼 활성화

**관리자 화면**:
- `admin_order_view.dart`: 목록에서 상태 표시
- `admin_order_detail_view.dart`: 상세 화면에서 상태 표시

---

## 📝 구현 계획

### Phase 1: 공용 유틸리티 클래스 생성 ✅
- [x] `OrderStatusUtils` 클래스 생성
- [x] `parseStatusToNumber` 함수 구현
- [x] 날짜 비교 헬퍼 함수 구현
- [x] `determineOrderStatus` 함수 구현

### Phase 2: 고객 화면 적용 ✅
- [x] `order_list_view.dart` 수정
- [x] `order_detail_view.dart` 수정
- [x] 30일 경과 자동 업데이트 로직 적용
- [x] 버튼 상태 표시 개선 (상태에 따라 버튼 텍스트 동적 변경)

### Phase 3: 관리자 화면 적용 ✅
- [x] `admin_order_view.dart` 수정
- [x] `admin_order_detail_view.dart` 수정

### Phase 4: 정리 및 테스트 ✅
- [x] 기존 중복 코드 제거
- [x] 테스트 및 검증
- [x] `isPickupDatePassed` 함수 추가 (pickupDate가 지난 경우 처리)

### Phase 5: 추가 개선 사항 (2025-12-17) ✅
- [x] `pickupDate`가 오늘보다 작거나 같을 때도 "제품 준비 완료" 상태로 처리하도록 개선
  - 기존: `pickupDate == 오늘`일 때만 처리
  - 개선: `pickupDate <= 오늘`일 때 처리
- [x] 주문 상세 뷰 버튼 텍스트를 현재 주문 상태에 맞게 동적으로 표시

---

## ⚠️ 주의사항

1. **날짜 비교 정확성**: ISO8601 형식의 문자열을 정확히 파싱하고 날짜만 비교
2. **상태 업데이트**: 30일 경과 시 DB에 실제로 업데이트해야 함 (현재는 표시만 변경)
3. **반품 상태 보호**: 반품 상태(3 이상)는 날짜 기반 자동 변경에서 제외
4. **고객/관리자 구분**: 관리자 화면에서는 실제 상태를 그대로 표시할 수도 있음 (옵션으로 제어)

---

**문서 버전**: 1.2  
**최종 수정일**: 2025-12-17  
**검토 완료일**: 2025-12-17

---

## ✅ 구현 상태 검토 (2025-12-17)

### 구현 완료된 항목

1. **공용 유틸리티 클래스** ✅
   - `OrderStatusUtils` 클래스 생성 완료
   - 모든 주요 함수 구현 완료

2. **주문 상태 결정 로직** ✅
   - 우선순위 순서 정확히 구현됨 (반품 상태 → 날짜 기반 → 아이템 상태)
   - `pickupDate <= 오늘` 로직 정확히 구현됨
   - 30일 경과 자동 수령 완료 로직 구현됨

3. **Purchase 객체 생성** ✅
   - `purchase_view.dart`에서 문서에 명시된 대로 구현됨
   - `timeStamp`: `now.toIso8601String()` ✅
   - `pickupDate`: `tomorrow.toIso8601String().split('T').first` ✅
   - `orderCode`: `OrderUtils.generateOrderCode(userId)` ✅

4. **화면 적용** ✅
   - 고객 화면 (`order_list_view.dart`, `order_detail_view.dart`) 적용 완료
   - 관리자 화면 (`admin_order_view.dart`, `admin_order_detail_view.dart`) 적용 완료
   - 30일 경과 자동 업데이트 로직 적용 완료

### 문서 업데이트 필요 사항

1. **함수 목록 보완**
   - `shouldAutoUpdateToReady` 함수는 실제로는 내부 헬퍼 함수로 처리됨
   - `isPickupDatePassed30Days`, `isPurchaseDateToday` 등 추가 함수 명시 필요
   - `determineReturnStatus` 함수 추가 필요

2. **내부 구현 세부사항**
   - `_getDateBasedStatusWithParsedDate` 내부 로직 설명 추가
   - 날짜 비교 방식 (`DateTime.isBefore`, `DateTime.isAtSameMomentAs`) 명시

---

## 📝 최근 업데이트 (2025-12-17)

### 1. 주문 상세 뷰 버튼 상태 표시 개선
- **파일**: `lib/view/cheng/screens/customer/order_detail_view.dart`
- **변경 사항**: 하단 버튼의 텍스트가 현재 주문 상태에 맞게 동적으로 표시되도록 개선
  - 기존: 항상 "픽업 완료" 텍스트로 고정
  - 개선: 현재 `_orderStatus` 값을 버튼 텍스트로 사용하여 상태와 일치

### 2. 결제 시 Purchase 객체 생성 로직 추가
- **파일**: `lib/view/customer/purchase_view.dart`
- **변경 사항**:
  - 결제 시 `Purchase` 객체를 자동 생성
  - `timeStamp`: `DateTime.now().toIso8601String()` (현재 날짜/시간)
  - `pickupDate`: `DateTime.now().add(Duration(days: 1)).toIso8601String().split('T').first` (현재 날짜 + 1일)
  - `orderCode`: `OrderUtils.generateOrderCode(userId)` 사용
  - `UserStorage.getUserId()`로 현재 로그인한 사용자 ID 가져오기

### 3. 주문 상태 결정 로직 추가 개선
- **파일**: `lib/utils/order_status_utils.dart`
- **변경 사항**:
  - `_getDateBasedStatusWithParsedDate` 내부에서 `pickupDate`가 오늘보다 작거나 같을 때 "제품 준비 완료" 상태로 처리
  - `DateTime.isBefore()` 또는 `DateTime.isAtSameMomentAs()` 사용하여 날짜 비교
  - 이제 `pickupDate`가 지난 경우에도 "제품 준비 완료" 상태로 정상 표시됨

### 4. 반품 상태 결정 함수 추가
- **파일**: `lib/utils/order_status_utils.dart`
- **변경 사항**:
  - `determineReturnStatus(...)` 함수 추가: 반품 가능 여부를 결정하는 함수
  - 반품 가능 조건: 상태가 2 (제품 수령 완료)이고 30일이 지나지 않은 경우
  - 반환값: "반품 가능" 또는 "반품 불가"

