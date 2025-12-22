import 'package:shoes_store_app/view/cheng/widgets/admin/base_order_card.dart';

/// 주문 관리용 주문 카드 위젯
/// 주문 관리 화면에서 사용하는 주문 카드입니다.
/// BaseOrderCard를 상속받아 구현되었으며, 주문 관리 화면에 특화된 기능을 제공합니다.
class OrderCard extends BaseOrderCard {
  /// 주문 카드 생성자
  /// [orderId] 주문 ID (주문 번호)
  /// [customerName] 고객 이름
  /// [orderStatus] 주문 상태
  /// [isSelected] 선택 여부
  /// [onTap] 클릭 콜백 함수
  const OrderCard({
    super.key,
    required super.orderId,
    required super.customerName,
    required super.orderStatus,
    required super.isSelected,
    required super.onTap,
  });
}

