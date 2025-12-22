import 'package:flutter/material.dart';
import 'package:shoes_store_app/view/cheng/custom/custom.dart';
import 'package:shoes_store_app/utils/order_status_colors.dart';

/// 주문 카드 기본 위젯
/// 주문 관리와 반품 관리 화면에서 공통으로 사용하는 카드 구조를 제공하는 베이스 클래스입니다.
/// 이 클래스를 상속받아 주문 카드(OrderCard)와 반품 카드(ReturnOrderCard)를 구현합니다.
class BaseOrderCard extends StatelessWidget {
  /// 주문 ID (주문 번호)
  final String orderId;
  /// 고객 이름
  final String customerName;
  /// 주문 상태 (예: 대기중, 준비완료, 반품요청 등)
  final String orderStatus;
  /// 현재 카드가 선택된 상태인지 여부
  final bool isSelected;
  /// 카드 클릭 시 실행될 콜백 함수
  final VoidCallback onTap;

  const BaseOrderCard({
    super.key,
    required this.orderId,
    required this.customerName,
    required this.orderStatus,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      // 카드 전체를 탭 가능하게 만듦
      onTap: onTap,
      child: CustomCard(
        // 선택된 상태일 때 배경색 변경
        color: isSelected ? Colors.blue.shade50 : null,
        margin: const EdgeInsets.only(bottom: 8),
        padding: const EdgeInsets.all(12),
        child: CustomColumn(
          crossAxisAlignment: CrossAxisAlignment.start,
          spacing: 8,
          children: [
            // 주문 ID와 상태를 한 줄에 표시
            CustomRow(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                // 주문 ID (굵은 글씨)
                CustomText(orderId, fontSize: 14, fontWeight: FontWeight.bold),
                // 주문 상태 (배지 형태로 표시)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: OrderStatusColors.getStatusColor(orderStatus),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: CustomText(
                  orderStatus,
                  fontSize: 12,
                  fontWeight: FontWeight.normal,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
            // 고객 이름 표시
            CustomText(
              customerName,
              fontSize: 14,
              fontWeight: FontWeight.normal,
            ),
          ],
        ),
      ),
    );
  }
}

