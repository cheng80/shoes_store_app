import 'package:shoes_store_app/core/global_storage.dart';

/// 장바구니 저장소 클래스
/// GlobalStorage를 사용하여 장바구니 정보를 저장하고 불러오는 기능을 제공합니다.
/// 메모리 기반 휘발성 저장소이므로 앱을 종료하면 데이터가 사라집니다.
/// 재고는 실제 구매 완료 시에만 차감되므로, 장바구니는 재고에 영향을 주지 않습니다.

class CartStorage {
  /// GlobalStorage 인스턴스
  static GlobalStorage get _storage => GlobalStorage.instance;

  /// 저장 키 상수
  static const String _keyCart = 'cart';

  /// 장바구니 저장
  /// 
  /// [cart] 저장할 장바구니 리스트 (List<Map<String, dynamic>>)
  /// 
  /// 사용 예시:
  /// ```dart
  /// final cart = [
  ///   {'productId': 1, 'quantity': 2, 'unitPrice': 10000, ...},
  ///   {'productId': 2, 'quantity': 1, 'unitPrice': 20000, ...},
  /// ];
  /// CartStorage.saveCart(cart);
  /// ```
  static void saveCart(List<Map<String, dynamic>> cart) {
    _storage.save(_keyCart, cart);
  }

  /// 장바구니 가져오기
  /// 
  /// 반환값: 저장된 장바구니 리스트, 없으면 빈 리스트
  /// 
  /// 사용 예시:
  /// ```dart
  /// final cart = CartStorage.getCart();
  /// if (cart.isNotEmpty) {
  ///   // 장바구니 처리
  /// }
  /// ```
  static List<Map<String, dynamic>> getCart() {
    final cart = _storage.get<List>(_keyCart);
    if (cart == null) return [];

    // 안전하게 Map 리스트로 변환
    return cart.map<Map<String, dynamic>>((e) {
      if (e is Map<String, dynamic>) return e;
      return Map<String, dynamic>.from(e as Map);
    }).toList();
  }

  /// 장바구니 비우기
  /// 
  /// 장바구니의 모든 항목을 삭제합니다.
  /// 
  /// 사용 예시:
  /// ```dart
  /// CartStorage.clearCart();
  /// ```
  static void clearCart() {
    _storage.remove(_keyCart);
  }

  /// 장바구니에 항목 추가
  /// 
  /// [item] 추가할 장바구니 항목 (Map<String, dynamic>)
  /// 
  /// 같은 제품이 이미 장바구니에 있으면 수량을 누적하고,
  /// 없으면 새로 추가합니다.
  /// 
  /// 사용 예시:
  /// ```dart
  /// final item = {
  ///   'productId': 1,
  ///   'quantity': 2,
  ///   'unitPrice': 10000,
  ///   'name': '나이키 에어맥스',
  ///   ...
  /// };
  /// CartStorage.addToCart(item);
  /// ```
  static void addToCart(Map<String, dynamic> item) {
    final cart = getCart();
    final productId = item['productId'];

    // 같은 제품이 이미 장바구니에 있는지 확인
    final idx = cart.indexWhere(
      (e) => e['productId'] == productId,
    );

    if (idx >= 0) {
      // 기존 항목의 수량 누적
      final currentQty = _asInt(cart[idx]['quantity'], 0);
      final newQty = _asInt(item['quantity'], 0);
      cart[idx]['quantity'] = currentQty + newQty;
    } else {
      // 새 항목 추가
      cart.add(item);
    }

    saveCart(cart);
  }

  /// 장바구니에서 항목 제거
  /// 
  /// [index] 제거할 항목의 인덱스
  /// 
  /// 사용 예시:
  /// ```dart
  /// CartStorage.removeFromCart(0); // 첫 번째 항목 제거
  /// ```
  static void removeFromCart(int index) {
    final cart = getCart();
    if (index >= 0 && index < cart.length) {
      cart.removeAt(index);
      saveCart(cart);
    }
  }

  /// 장바구니 항목 수량 업데이트
  /// 
  /// [index] 업데이트할 항목의 인덱스
  /// [quantity] 새로운 수량
  /// 
  /// 사용 예시:
  /// ```dart
  /// CartStorage.updateQuantity(0, 5); // 첫 번째 항목의 수량을 5로 변경
  /// ```
  static void updateQuantity(int index, int quantity) {
    final cart = getCart();
    if (index >= 0 && index < cart.length && quantity > 0) {
      cart[index]['quantity'] = quantity;
      saveCart(cart);
    }
  }

  /// 장바구니가 비어있는지 확인
  /// 
  /// 반환값: 장바구니가 비어있으면 true, 아니면 false
  /// 
  /// 사용 예시:
  /// ```dart
  /// if (CartStorage.isEmpty()) {
  ///   print('장바구니가 비어있습니다');
  /// }
  /// ```
  static bool isEmpty() {
    return getCart().isEmpty;
  }

  /// 장바구니 항목 개수 가져오기
  /// 
  /// 반환값: 장바구니에 담긴 항목 개수
  /// 
  /// 사용 예시:
  /// ```dart
  /// final count = CartStorage.getItemCount();
  /// print('장바구니 항목 수: $count');
  /// ```
  static int getItemCount() {
    return getCart().length;
  }

  /// 동적 값을 int로 변환하는 헬퍼 메서드
  static int _asInt(dynamic v, [int def = 0]) {
    if (v == null) return def;
    if (v is int) return v;
    if (v is num) return v.toInt();
    if (v is String) return int.tryParse(v) ?? def;
    return def;
  }
}

