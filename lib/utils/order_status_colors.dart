// Flutter imports
import 'package:flutter/material.dart';

// Local imports - Core
import 'package:shoes_store_app/config.dart' as config;

/// 주문 상태별 색상 유틸리티
/// 관리자와 고객 페이지에서 공통으로 사용하는 주문 상태 색상을 제공합니다.
class OrderStatusColors {
  /// 주문 상태에 따른 색상 반환
  /// config.dart의 pickupStatus를 참고하여 색상을 결정합니다.
  /// 
  /// 상태별 색상:
  /// - 제품 준비 중 (0): 주황색
  /// - 제품 준비 완료 (1): 파란색
  /// - 제품 수령 완료 (2): 회색
  /// - 반품 신청 (3): 빨간색
  /// - 반품 처리 중 (4): 보라색
  /// - 반품 완료 (5): 검은색
  /// - 반품 가능: 초록색
  /// - 반품 불가: 회색
  /// 
  /// [status] 주문 상태 문자열 (예: '제품 준비 중', '제품 준비 완료', '제품 수령 완료', '반품 가능', '반품 불가')
  /// 반환값: 해당 상태에 맞는 색상
  static Color getStatusColor(String status) {
    // 반품 가능/불가 상태 처리
    if (status == '반품 가능') {
      return Colors.green;
    } else if (status == '반품 불가') {
      return Colors.grey;
    }
    
    // config.pickupStatus의 밸류와 직접 비교
    for (var entry in config.pickupStatus.entries) {
      if (status == entry.value) {
        return _getColorByStatusNumber(entry.key);
      }
    }
    
    // 키워드로 매핑 (하위 호환성)
    final lowerStatus = status.toLowerCase();
    
    if (lowerStatus.contains('반품 완료') || lowerStatus.contains('return done')) {
      return _getColorByStatusNumber(5);
    } else if (lowerStatus.contains('반품 처리') || lowerStatus.contains('return processing')) {
      return _getColorByStatusNumber(4);
    } else if (lowerStatus.contains('반품 신청') || lowerStatus.contains('return request')) {
      return _getColorByStatusNumber(3);
    } else if (lowerStatus.contains('수령 완료') || lowerStatus.contains('complete')) {
      return _getColorByStatusNumber(2);
    } else if (lowerStatus.contains('준비 완료') || lowerStatus.contains('ready') || lowerStatus.contains('onway')) {
      return _getColorByStatusNumber(1);
    } else if (lowerStatus.contains('준비 중') || lowerStatus.contains('대기')) {
      return _getColorByStatusNumber(0);
    }
    
    // 기본값: 회색
    return Colors.grey;
  }

  /// 상태 번호에 따른 색상 반환
  /// 
  /// [statusNumber] 상태 번호 (0: 제품 준비 중, 1: 제품 준비 완료, 2: 제품 수령 완료, 3: 반품 신청, 4: 반품 처리 중, 5: 반품 완료)
  /// 반환값: 해당 상태에 맞는 색상
  static Color _getColorByStatusNumber(int statusNumber) {
    switch (statusNumber) {
      case 0: // 제품 준비 중
        return Colors.orange;
      case 1: // 제품 준비 완료
        return Colors.blue;
      case 2: // 제품 수령 완료
        return Colors.grey;
      case 3: // 반품 신청
        return Colors.red;
      case 4: // 반품 처리 중
        return Colors.purple;
      case 5: // 반품 완료
        return Colors.black;
      default:
        return Colors.grey;
    }
  }
}

