import 'package:intl/intl.dart';

/// 주문 관련 유틸리티 함수들
/// 
/// 주문 관리 화면에서 공통으로 사용하는 유틸리티 함수들을 제공합니다.
class OrderUtils {
  /// 주문 코드 생성
  /// 
  /// 유저 ID와 현재 날짜/시간을 조합하여 고유한 주문 코드를 생성합니다.
  /// 형식: {userId}_{yyyyMMddHHmmss}
  /// 
  /// 예시:
  /// - userId: 1, 시간: 2025-12-13 14:30:25 → "1_20251213143025"
  /// - userId: 5, 시간: 2025-12-13 09:15:00 → "5_20251213091500"
  /// 
  /// [userId] 고객 ID
  /// 반환: 생성된 주문 코드 문자열
  static String generateOrderCode(int userId) {
    final now = DateTime.now();
    final dateTimeStr = DateFormat('yyyyMMddHHmmss').format(now);
    return '${userId}_$dateTimeStr';
  }

  /// 가격 포맷팅 함수 (천 단위 콤마 추가)
  /// 
  /// 정수형 가격을 받아서 천 단위 콤마가 포함된 문자열로 변환합니다.
  /// 
  /// 예시:
  /// - 120000 → "120,000"
  /// - 5000 → "5,000"
  /// 
  /// [price] 포맷팅할 가격 (정수)
  /// 반환: 천 단위 콤마가 포함된 가격 문자열
  static String formatPrice(int price) {
    return price.toString().replaceAllMapped(
      RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'),
      (Match m) => '${m[1]},',
    );
  }
}

