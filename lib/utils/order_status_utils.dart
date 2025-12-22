import 'package:shoes_store_app/config.dart' as config;
import 'package:shoes_store_app/model/sale/purchase.dart';
import 'package:shoes_store_app/model/sale/purchase_item.dart';
import 'package:shoes_store_app/utils/app_logger.dart';

/// 주문 상태 관련 유틸리티 함수들
/// 
/// 주문 상태 결정, 파싱, 날짜 비교 등의 공통 로직을 제공합니다.
/// 고객 화면과 관리자 화면에서 공통으로 사용합니다.
class OrderStatusUtils {
  /// pcStatus를 숫자로 변환
  /// 
  /// config.pickupStatus의 value(한글 문자열)와 비교하여 숫자로 변환합니다.
  /// DB에는 value(한글 문자열)만 저장되므로 value 비교만 수행합니다.
  /// 
  /// 지원 형식:
  /// - 상태 문자열: '제품 준비 중', '제품 준비 완료', '제품 수령 완료', '반품 신청', '반품 처리 중', '반품 완료'
  /// 
  /// [pcStatus] PurchaseItem의 pcStatus 값 (한글 문자열)
  /// 반환: 상태 번호 (0~5), 파싱 실패 시 0 반환 (로그 기록)
  static int parseStatusToNumber(String pcStatus) {
    // pickupStatus의 value(한글 문자열)와 직접 비교
    for (var entry in config.pickupStatus.entries) {
      if (pcStatus == entry.value) {
        return entry.key;
      }
    }
    
    // 알 수 없는 상태 문자열인 경우 로그 기록 후 기본값 반환
    AppLogger.w('알 수 없는 상태 문자열: "$pcStatus" - 기본값 0(제품 준비 중) 반환', tag: 'OrderStatusUtils');
    return 0;
  }

  /// 날짜 문자열에서 날짜 부분만 추출 (시간 제외)
  /// 
  /// ISO8601 형식의 문자열에서 YYYY-MM-DD 부분만 추출합니다.
  /// 
  /// 예시:
  /// - '2025-12-13 14:30:25' → '2025-12-13'
  /// - '2025-12-13T14:30:25.000Z' → '2025-12-13'
  /// 
  /// [dateTimeString] ISO8601 형식의 날짜 문자열
  /// 반환: 날짜 부분만 포함한 문자열, 파싱 실패 시 null (로그 기록)
  static String? extractDateOnly(String dateTimeString) {
    if (dateTimeString.isEmpty) {
      AppLogger.w('빈 날짜 문자열이 전달됨', tag: 'OrderStatusUtils');
      return null;
    }

    // DateTime.parse가 실패할 수 있는 경우를 명시적으로 처리
    final dateTime = DateTime.tryParse(dateTimeString);
    if (dateTime == null) {
      AppLogger.w('날짜 파싱 실패: "$dateTimeString"', tag: 'OrderStatusUtils');
      return null;
    }

    return '${dateTime.year}-${dateTime.month.toString().padLeft(2, '0')}-${dateTime.day.toString().padLeft(2, '0')}';
  }

  /// 두 날짜 문자열이 같은 날인지 확인 (시간 제외)
  /// 
  /// [dateString1] 첫 번째 날짜 문자열
  /// [dateString2] 두 번째 날짜 문자열
  /// 반환: 같은 날이면 true, 아니면 false
  static bool isSameDate(String dateString1, String dateString2) {
    final date1 = extractDateOnly(dateString1);
    final date2 = extractDateOnly(dateString2);
    if (date1 == null || date2 == null) return false;
    return date1 == date2;
  }

  /// 구매 당일인지 확인 (timeStamp와 오늘 날짜 비교)
  /// 
  /// [purchase] Purchase 객체
  /// [now] 현재 시각 (테스트 가능하도록 파라미터로 받음)
  /// 반환: 구매 당일이면 true
  static bool isPurchaseDateToday(Purchase purchase, DateTime now) {
    return isSameDate(purchase.timeStamp, now.toIso8601String());
  }

  /// 픽업 날짜로부터 30일 이상 경과했는지 확인
  /// 
  /// [purchase] Purchase 객체
  /// [now] 현재 시각 (테스트 가능하도록 파라미터로 받음)
  /// 반환: 30일 이상 경과했으면 true, 파싱 실패 시 false (로그 기록)
  static bool isPickupDatePassed30Days(Purchase purchase, DateTime now) {
    if (purchase.pickupDate.isEmpty) {
      AppLogger.w('pickupDate가 비어있음 - Purchase ID: ${purchase.id}', tag: 'OrderStatusUtils');
      return false;
    }

    final pickupDate = DateTime.tryParse(purchase.pickupDate);
    if (pickupDate == null) {
      AppLogger.w('pickupDate 파싱 실패: "${purchase.pickupDate}" - Purchase ID: ${purchase.id}', tag: 'OrderStatusUtils');
      return false;
    }

    final daysDifference = now.difference(pickupDate).inDays;
    return daysDifference >= 30;
  }

  /// 반품 상태(3 이상)가 있는지 확인
  /// 
  /// [items] PurchaseItem 리스트
  /// 반환: 반품 상태가 하나라도 있으면 true
  static bool hasReturnStatus(List<PurchaseItem> items) {
    return items.any((item) {
      final statusNum = parseStatusToNumber(item.pcStatus);
      return statusNum >= 3;
    });
  }

  /// 주문 상태 결정 (고객 화면용)
  /// 
  /// 상태 결정 순서 (우선순위 높은 순):
  /// 1. 빈 아이템 목록 → 기본값 반환
  /// 2. 반품 상태 있음 → 반품 상태 반환
  /// 3. 날짜 기반 자동 변경 → 날짜 조건에 맞는 상태 반환
  /// 4. PurchaseItem의 pcStatus → 아이템 상태 기반으로 결정
  /// 
  /// 이 순서는 중요한 이유:
  /// - 반품 상태는 날짜와 관계없이 최우선
  /// - 날짜 기반 자동 변경은 실제 상태보다 우선
  /// - 마지막으로 실제 아이템 상태를 확인
  /// 
  /// [items] PurchaseItem 리스트
  /// [purchase] Purchase 객체
  /// [now] 현재 시각 (기본값: DateTime.now())
  /// 반환: 결정된 상태 문자열
  static String determineOrderStatusForCustomer(
    List<PurchaseItem> items,
    Purchase purchase, {
    DateTime? now,
  }) {
    final currentTime = now ?? DateTime.now();

    // 1단계: 빈 아이템 목록 체크
    if (items.isEmpty) {
      AppLogger.e(
        '주문 상태 결정 실패: PurchaseItem 목록이 비어있음 (데이터 무결성 오류) - Purchase ID: ${purchase.id}, OrderCode: ${purchase.orderCode}',
        tag: 'OrderStatusUtils',
      );
      return config.pickupStatus[0] ?? config.pickupStatus[0]!; // '제품 준비 중'
    }

    // 2단계: 반품 상태 체크 (최우선)
    final returnStatus = _getReturnStatusIfExists(items, purchase);
    if (returnStatus != null) {
      return returnStatus;
    }

    // 3단계: 날짜 기반 자동 상태 변경 체크
    // pickupDate 파싱을 한 번만 수행 (중복 체크 제거)
    final parsedPickupDate = _parsePickupDate(purchase);
    final dateBasedStatus = _getDateBasedStatusWithParsedDate(
      purchase,
      parsedPickupDate,
      currentTime,
    );
    if (dateBasedStatus != null) {
      return dateBasedStatus;
    }

    // 4단계: PurchaseItem의 pcStatus 기반 결정
    return _getStatusFromItems(items, purchase, isCustomerView: true);
  }

  /// 주문 상태 결정 (관리자 화면용)
  /// 
  /// 상태 결정 순서는 고객 화면과 동일하며, showActualStatus 옵션에 따라 실제 상태 표시 여부가 결정됩니다.
  /// 
  /// [items] PurchaseItem 리스트
  /// [purchase] Purchase 객체
  /// [now] 현재 시각 (기본값: DateTime.now())
  /// [showActualStatus] true면 실제 상태 그대로 표시, false면 고객 화면과 동일 (기본값: true)
  /// 반환: 결정된 상태 문자열
  static String determineOrderStatusForAdmin(
    List<PurchaseItem> items,
    Purchase purchase, {
    DateTime? now,
    bool showActualStatus = true,
  }) {
    final currentTime = now ?? DateTime.now();

    // 1단계: 빈 아이템 목록 체크
    if (items.isEmpty) {
      AppLogger.e(
        '주문 상태 결정 실패(관리자): PurchaseItem 목록이 비어있음 (데이터 무결성 오류) - Purchase ID: ${purchase.id}, OrderCode: ${purchase.orderCode}',
        tag: 'OrderStatusUtils',
      );
      return config.pickupStatus[0] ?? config.pickupStatus[0]!; // '제품 준비 중'
    }

    // 2단계: 반품 상태 체크 (최우선)
    final returnStatus = _getReturnStatusIfExists(items, purchase);
    if (returnStatus != null) {
      return returnStatus;
    }

    // 3단계: 날짜 기반 자동 상태 변경 체크
    // pickupDate 파싱을 한 번만 수행 (중복 체크 제거)
    final parsedPickupDate = _parsePickupDate(purchase);
    final dateBasedStatus = _getDateBasedStatusWithParsedDate(
      purchase,
      parsedPickupDate,
      currentTime,
    );
    if (dateBasedStatus != null) {
      return dateBasedStatus;
    }

    // 4단계: PurchaseItem의 pcStatus 기반 결정
    return _getStatusFromItems(items, purchase, isCustomerView: !showActualStatus);
  }

  /// 30일 경과로 인한 자동 수령 완료 처리 여부 확인
  /// 
  /// [items] PurchaseItem 리스트
  /// [purchase] Purchase 객체
  /// [now] 현재 시각 (기본값: DateTime.now())
  /// 반환: 자동 수령 완료 처리해야 하면 true
  static bool shouldAutoUpdateToCompleted(
    List<PurchaseItem> items,
    Purchase purchase, {
    DateTime? now,
  }) {
    final currentTime = now ?? DateTime.now();
    
    // 반품 상태가 있으면 자동 변경 불가
    if (hasReturnStatus(items)) {
      return false;
    }
    
    // 30일 경과 확인
    if (!isPickupDatePassed30Days(purchase, currentTime)) {
      return false;
    }
    
    // 이미 status 2 이상인 아이템만 있는지 확인
    // 하나라도 status 2 미만이 있으면 업데이트 필요
    return items.any((item) {
      final statusNum = parseStatusToNumber(item.pcStatus);
      return statusNum < 2;
    });
  }

  // ========== 헬퍼 함수들 (각 단계별로 분리) ==========

  /// 반품 상태가 있으면 반품 상태를 반환, 없으면 null
  /// 
  /// 반품 상태(3 이상)가 하나라도 있으면 가장 높은 반품 상태를 반환합니다.
  /// 반품 상태가 없으면 null을 반환하여 다음 단계로 진행합니다.
  /// 
  /// [items] PurchaseItem 리스트
  /// [purchase] Purchase 객체
  /// 반환: 반품 상태가 있으면 상태 문자열, 없으면 null
  static String? _getReturnStatusIfExists(
    List<PurchaseItem> items,
    Purchase purchase,
  ) {
    // 반품 상태가 있는지 확인
    if (!hasReturnStatus(items)) {
      return null; // 반품 상태가 아니면 null 반환 (다음 단계로 진행)
    }

    // 반품 상태 중 가장 높은 상태 찾기
    final statusNumbers = items
        .map((item) => parseStatusToNumber(item.pcStatus))
        .where((status) => status >= 3) // 반품 상태만 필터링
        .toList();

    if (statusNumbers.isEmpty) {
      return null;
    }

    final maxReturnStatus = statusNumbers.reduce((a, b) => a > b ? a : b);

    // 유효한 반품 상태 범위 체크
    if (maxReturnStatus >= 3 && maxReturnStatus <= 5) {
      return config.pickupStatus[maxReturnStatus] ?? config.pickupStatus[3]!; // '반품 신청'
    }

    // 예상치 못한 상태 번호
    AppLogger.w(
      '예상치 못한 반품 상태 번호 - Purchase ID: ${purchase.id}, Status: $maxReturnStatus',
      tag: 'OrderStatusUtils',
    );
    return config.pickupStatus[0] ?? config.pickupStatus[0]!; // '제품 준비 중'
  }

  /// pickupDate 파싱 (중복 체크 제거를 위한 헬퍼 함수)
  /// 
  /// [purchase] Purchase 객체
  /// 반환: 파싱된 DateTime 객체, 파싱 실패 시 null
  static DateTime? _parsePickupDate(Purchase purchase) {
    if (purchase.pickupDate.isEmpty) {
      AppLogger.w(
        'pickupDate가 비어있음 - Purchase ID: ${purchase.id}',
        tag: 'OrderStatusUtils',
      );
      return null;
    }

    final pickupDate = DateTime.tryParse(purchase.pickupDate);
    if (pickupDate == null) {
      AppLogger.w(
        'pickupDate 파싱 실패: "${purchase.pickupDate}" - Purchase ID: ${purchase.id}',
        tag: 'OrderStatusUtils',
      );
      return null;
    }

    return pickupDate;
  }

  /// 날짜 기반 자동 상태 변경 체크 (파싱된 DateTime 사용)
  /// 
  /// 우선순위 순서:
  /// 1. 30일 경과 → "제품 수령 완료" (status 2)
  /// 2. 픽업 날짜 경과 → "제품 준비 완료" (status 1)
  /// 3. 구매 당일 → "제품 준비 중" (status 0)
  /// 
  /// 조건에 맞지 않으면 null을 반환하여 다음 단계로 진행합니다.
  /// 
  /// [purchase] Purchase 객체
  /// [parsedPickupDate] 이미 파싱된 pickupDate (null일 수 있음)
  /// [now] 현재 시각
  /// 반환: 날짜 조건에 맞는 상태 문자열, 조건에 맞지 않으면 null
  static String? _getDateBasedStatusWithParsedDate(
    Purchase purchase,
    DateTime? parsedPickupDate,
    DateTime now,
  ) {
    // 우선순위 1: 30일 경과 체크
    if (parsedPickupDate != null) {
      final daysDifference = now.difference(parsedPickupDate).inDays;
      if (daysDifference >= 30) {
        return config.pickupStatus[2] ?? config.pickupStatus[2]!; // '제품 수령 완료'
      }
    }

    // 우선순위 2: 픽업 날짜 경과 체크
    if (parsedPickupDate != null) {
      // 날짜만 비교 (시간 제외)
      final pickupDateOnly = DateTime(
        parsedPickupDate.year,
        parsedPickupDate.month,
        parsedPickupDate.day,
      );
      final nowDateOnly = DateTime(now.year, now.month, now.day);

      // pickupDate가 오늘보다 작거나 같으면 true
      if (pickupDateOnly.isBefore(nowDateOnly) ||
          pickupDateOnly.isAtSameMomentAs(nowDateOnly)) {
        return config.pickupStatus[1] ?? config.pickupStatus[1]!; // '제품 준비 완료'
      }
    }

    // 우선순위 3: 구매 당일 체크
    if (isPurchaseDateToday(purchase, now)) {
      return config.pickupStatus[0] ?? config.pickupStatus[0]!; // '제품 준비 중'
    }

    // 날짜 기반 조건에 맞지 않으면 null 반환 (다음 단계로 진행)
    return null;
  }


  /// PurchaseItem의 pcStatus 기반으로 상태 결정
  /// 
  /// 모든 아이템의 상태를 확인하여 최종 상태를 결정합니다.
  /// - 모든 아이템이 같은 상태면 그 상태 사용
  /// - 아이템 상태가 다르면 가장 낮은 상태 사용 (보수적 접근)
  /// 
  /// [isCustomerView] true면 고객 화면용 (status 2 이상은 모두 "제품 수령 완료"),
  ///                  false면 관리자 화면용 (실제 상태 그대로 표시)
  /// 
  /// [items] PurchaseItem 리스트
  /// [purchase] Purchase 객체
  /// [isCustomerView] 고객 화면용 여부
  /// 반환: 결정된 상태 문자열
  static String _getStatusFromItems(
    List<PurchaseItem> items,
    Purchase purchase, {
    required bool isCustomerView,
  }) {
    // 모든 아이템의 상태 번호 추출
    final statusNumbers = items
        .map((item) => parseStatusToNumber(item.pcStatus))
        .toList();

    // 모든 아이템이 같은 상태인지 확인
    final firstStatus = statusNumbers.first;
    final allSameStatus = statusNumbers.every((status) => status == firstStatus);

    // 상태 결정: 모든 아이템이 같은 상태면 그 상태 사용,
    //            다르면 가장 낮은 상태 사용 (보수적 접근)
    final displayStatus = allSameStatus
        ? firstStatus
        : statusNumbers.reduce((a, b) => a < b ? a : b);

    // 고객 화면용 처리
    if (isCustomerView) {
      // status 2 이상은 모두 "제품 수령 완료"로 표시
      if (displayStatus >= 2 && displayStatus <= 5) {
        return config.pickupStatus[2] ?? config.pickupStatus[2]!; // '제품 수령 완료'
      } else if (displayStatus == 0 || displayStatus == 1) {
        return config.pickupStatus[displayStatus] ?? config.pickupStatus[0]!; // '제품 준비 중'
      } else {
        AppLogger.w(
          '예상치 못한 상태 번호 - Purchase ID: ${purchase.id}, Status: $displayStatus',
          tag: 'OrderStatusUtils',
        );
        return config.pickupStatus[0] ?? config.pickupStatus[0]!; // '제품 준비 중'
      }
    }

    // 관리자 화면용 처리 (실제 상태 그대로 표시)
    if (displayStatus >= 0 && displayStatus <= 5) {
      return config.pickupStatus[displayStatus] ?? config.pickupStatus[0]!; // '제품 준비 중'
    } else {
      AppLogger.w(
        '예상치 못한 상태 번호(관리자) - Purchase ID: ${purchase.id}, Status: $displayStatus',
        tag: 'OrderStatusUtils',
      );
      return config.pickupStatus[0] ?? config.pickupStatus[0]!; // '제품 준비 중'
    }
  }

  /// 반품 가능 여부를 결정하는 함수
  /// 
  /// 반품 가능 조건:
  /// - 상태가 2 (제품 수령 완료)이고
  /// - pickupDate로부터 30일이 지나지 않았으면 반품 가능
  /// 
  /// 반환값:
  /// - "반품 가능": 하나라도 반품 가능한 아이템이 있는 경우
  /// - "반품 불가": 모든 아이템이 반품 완료(5)이거나, 반품 가능한 아이템이 없는 경우
  /// 
  /// [items] PurchaseItem 리스트
  /// [purchase] Purchase 객체
  /// [now] 현재 시각 (기본값: DateTime.now())
  /// 반환: "반품 가능" 또는 "반품 불가"
  static String determineReturnStatus(
    List<PurchaseItem> items,
    Purchase purchase, {
    DateTime? now,
  }) {
    // 1. 빈 아이템 목록 처리 (데이터 무결성 오류)
    if (items.isEmpty) {
      AppLogger.e('반품 상태 결정 실패: PurchaseItem 목록이 비어있음 (데이터 무결성 오류) - Purchase ID: ${purchase.id}, OrderCode: ${purchase.orderCode}', tag: 'OrderStatusUtils');
      // 데이터 오류 상황이므로 "반품 불가" 반환 (호출하는 쪽에서 이 상황을 인지할 수 있도록 로그 기록)
      return '반품 불가';
    }

    final currentTime = now ?? DateTime.now();
    bool hasReturnableItem = false;
    bool allReturnCompleted = true;
    
    // 각 아이템의 상태를 순차적으로 확인
    for (final item in items) {
      final statusNum = parseStatusToNumber(item.pcStatus);
      
      // 반품 완료 상태(5) 확인
      if (statusNum == 5) {
        // 반품 완료 상태이면 계속 진행 (allReturnCompleted는 이미 true)
        continue;
      } else {
        // 반품 완료가 아닌 경우 allReturnCompleted를 false로 설정
        allReturnCompleted = false;
      }
      
      // 반품 가능 조건 확인: 상태가 2 (제품 수령 완료)이고 30일이 지나지 않았으면 반품 가능
      if (statusNum == 2) {
        final is30DaysPassed = isPickupDatePassed30Days(purchase, currentTime);
        if (!is30DaysPassed) {
          hasReturnableItem = true;
        }
      }
      // 상태가 0, 1, 3, 4인 경우는 반품 불가 (조건에 명시적으로 포함되지 않음)
    }

    // 최종 반품 가능 여부 결정
    // 모든 아이템이 반품 완료(5)이면 "반품 불가"
    if (allReturnCompleted) {
      return '반품 불가';
    }
    
    // 하나라도 반품 가능한 아이템이 있으면 "반품 가능"
    if (hasReturnableItem) {
      return '반품 가능';
    }

    // 그 외의 경우 (반품 신청, 반품 처리 중, 30일 경과 등) "반품 불가"
    return '반품 불가';
  }
}

