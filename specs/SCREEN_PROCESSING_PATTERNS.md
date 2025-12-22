# 화면 처리 패턴 가이드

**작성일**: 2025-12-17  
**목적**: 효율적이고 단순한 화면 로직 처리 패턴 제공

---

## 📌 문서 성격

이 문서는 **현재 코드베이스의 주요 패턴을 반영**하면서, 동시에 **앞으로 모든 화면에서 따라가야 할 가이드**입니다.

### 현재 상태
- ✅ 대부분의 화면이 이 패턴을 따르고 있음
- ✅ 핸들러 클래스 필드 선언, Map 캐싱, 유틸리티 함수 활용 등 적용됨
- ⚠️ 일부 화면에서 중첩된 try-catch나 개선 가능한 부분 존재

### 목표
- 모든 화면에서 일관된 패턴 적용
- 코드 가독성 및 유지보수성 향상
- 효율적인 데이터 처리

**새로운 화면을 작성하거나 기존 화면을 수정할 때 이 가이드를 참고하세요.**

---

## 핵심 원칙

### 1. 단순성 우선
- 복잡한 로직은 유틸리티 함수로 분리
- 중첩된 try-catch 지양
- 명시적 조건 체크로 가독성 향상

### 2. 효율성
- 불필요한 반복 조회 최소화
- Map을 활용한 데이터 캐싱
- 한 번의 조회로 필요한 데이터 수집

### 3. 일관성
- 모든 화면에서 동일한 패턴 사용
- 핸들러는 클래스 필드로 선언
- 데이터 로드는 initState에서 시작

---

## 기본 구조 패턴

### 화면 클래스 기본 구조

```dart
class MyScreen extends StatefulWidget {
  const MyScreen({super.key});

  @override
  State<MyScreen> createState() => _MyScreenState();
}

class _MyScreenState extends State<MyScreen> {
  // 1. 상태 변수
  List<Data> _dataList = [];
  bool _isLoading = true;
  
  // 2. 핸들러 (클래스 필드로 선언)
  final DataHandler _dataHandler = DataHandler();
  
  // 3. initState에서 데이터 로드
  @override
  void initState() {
    super.initState();
    _loadData();
  }
  
  // 4. 데이터 로드 함수 (단순한 try-catch)
  Future<void> _loadData() async {
    setState(() => _isLoading = true);
    
    try {
      final data = await _dataHandler.queryAll();
      setState(() {
        _dataList = data;
        _isLoading = false;
      });
    } catch (e, stackTrace) {
      AppLogger.e('데이터 로드 실패', error: e, stackTrace: stackTrace);
      setState(() {
        _dataList = [];
        _isLoading = false;
      });
    }
  }
  
  @override
  Widget build(BuildContext context) {
    // UI 구성
  }
}
```

---

## 데이터 로딩 패턴

### 패턴 1: 단순 조회

```dart
Future<void> _loadOrders() async {
  setState(() => _isLoading = true);
  
  try {
    final orders = await _purchaseHandler.queryByCustomerId(userId);
    setState(() {
      _orders = orders;
      _isLoading = false;
    });
  } catch (e, stackTrace) {
    AppLogger.e('주문 목록 로드 실패', error: e, stackTrace: stackTrace);
    setState(() {
      _orders = [];
      _isLoading = false;
    });
  }
}
```

### 패턴 2: 조인 쿼리 활용 (효율적)

```dart
Future<void> _loadProductData() async {
  setState(() => _loading = true);
  
  try {
    // 한 번의 조회로 필요한 데이터 수집
    final productsWithImages = await _productBaseHandler.queryListWithFirstImage();
    
    // Map으로 변환하여 효율적으로 관리
    final productMap = <int, ProductBase>{};
    final imageMap = <int, String>{};
    
    for (final map in productsWithImages) {
      final product = ProductBase.fromMap(map);
      if (product.id != null) {
        productMap[product.id!] = product;
        final image = map['firstImage'] as String?;
        if (image != null) {
          imageMap[product.id!] = image;
        }
      }
    }
    
    setState(() {
      _products = productMap.values.toList();
      _imageMap = imageMap;
      _loading = false;
    });
  } catch (e, stackTrace) {
    AppLogger.e('제품 데이터 로드 실패', error: e, stackTrace: stackTrace);
    setState(() => _loading = false);
  }
}
```

### 패턴 3: 복합 데이터 수집 (Map 활용)

```dart
Future<void> _loadOrdersWithStatus() async {
  setState(() => _isLoading = true);
  
  try {
    final purchases = await _purchaseHandler.queryAll();
    
    // Map으로 상태와 고객명 캐싱
    final statusMap = <int, String>{};
    final customerMap = <int, String>{};
    
    for (final purchase in purchases) {
      if (purchase.id == null) continue;
      
      // 상태 결정 (유틸리티 함수 활용)
      final items = await _purchaseItemHandler.queryByPurchaseId(purchase.id!);
      final status = OrderStatusUtils.determineOrderStatusForAdmin(items, purchase);
      statusMap[purchase.id!] = status;
      
      // 고객명 조회
      if (purchase.cid != null) {
        final customer = await _customerHandler.queryById(purchase.cid!);
        if (customer != null) {
          customerMap[purchase.id!] = customer.cName;
        }
      }
    }
    
    setState(() {
      _orders = purchases;
      _statusMap = statusMap;
      _customerMap = customerMap;
      _isLoading = false;
    });
  } catch (e, stackTrace) {
    AppLogger.e('주문 목록 로드 실패', error: e, stackTrace: stackTrace);
    setState(() => _isLoading = false);
  }
}
```

---

## 조건 처리 패턴

### 명시적 null 체크

```dart
// ✅ 좋은 예: 명시적 체크
if (purchase.id == null) {
  AppLogger.w('Purchase ID가 null: ${purchase.orderCode}');
  continue; // 또는 return
}

// ❌ 나쁜 예: 강제 언래핑
final id = purchase.id!; // 위험
```

### 유틸리티 함수 활용

```dart
// ✅ 좋은 예: 유틸리티 함수 사용
final status = OrderStatusUtils.determineOrderStatusForCustomer(items, purchase);
final statusNum = OrderStatusUtils.parseStatusToNumber(item.pcStatus);
final is30DaysPassed = OrderStatusUtils.isPickupDatePassed30Days(purchase, DateTime.now());

// ❌ 나쁜 예: 직접 구현 (중복 코드)
final pickupDate = DateTime.parse(purchase.pickupDate);
final daysDifference = DateTime.now().difference(pickupDate).inDays;
final is30DaysPassed = daysDifference >= 30;
```

### 조건 분기 (단순화)

```dart
// ✅ 좋은 예: 명확한 조건
String getStatusText(String status) {
  final statusNum = OrderStatusUtils.parseStatusToNumber(status);
  
  if (statusNum == 0) return config.pickupStatus[0]!; // '제품 준비 중'
  if (statusNum == 1) return config.pickupStatus[1]!; // '제품 준비 완료'
  if (statusNum >= 2) return config.pickupStatus[2]!; // '제품 수령 완료'
  
  AppLogger.w('예상치 못한 상태: $status');
  return config.pickupStatus[0]!; // 기본값
}
```

---

## 반복문 처리 패턴

### 효율적인 반복 처리

```dart
// ✅ 좋은 예: Map으로 중복 제거 및 효율적 처리
final statusMap = <int, String>{};

for (final purchase in purchases) {
  if (purchase.id == null) continue; // null 체크로 건너뛰기
  
  try {
    final items = await _purchaseItemHandler.queryByPurchaseId(purchase.id!);
    final status = OrderStatusUtils.determineOrderStatusForCustomer(items, purchase);
    statusMap[purchase.id!] = status;
  } catch (e) {
    AppLogger.e('주문 상태 조회 실패 (ID: ${purchase.id})', error: e);
    statusMap[purchase.id!] = config.pickupStatus[0]!; // 기본값
  }
}
```

### 데이터 필터링 (getter 활용)

```dart
// ✅ 좋은 예: getter로 필터링 로직 분리
List<Purchase> get _filteredOrders {
  final searchText = _searchController.text.toLowerCase();
  if (searchText.isEmpty) return _orders;
  
  return _orders.where((order) {
    if (order.orderCode.toLowerCase().contains(searchText)) return true;
    final customerName = _customerNameMap[order.id] ?? '';
    return customerName.toLowerCase().contains(searchText);
  }).toList();
}
```

---

## 상태 업데이트 패턴

### 단순한 상태 업데이트

```dart
// ✅ 좋은 예: 한 번의 setState로 모든 상태 업데이트
setState(() {
  _orders = purchases;
  _statusMap = statusMap;
  _isLoading = false;
});

// ❌ 나쁜 예: 여러 번의 setState
setState(() => _orders = purchases);
setState(() => _statusMap = statusMap);
setState(() => _isLoading = false);
```

### 조건부 상태 업데이트

```dart
// ✅ 좋은 예: 조건 확인 후 업데이트
if (userId == null) {
  AppLogger.w('사용자 정보가 없습니다.');
  setState(() {
    _orders = [];
    _isLoading = false;
  });
  return;
}
```

---

## 에러 처리 패턴

### 최상위 레벨 try-catch

```dart
// ✅ 좋은 예: 최상위 레벨에서만 try-catch
Future<void> _loadData() async {
  setState(() => _isLoading = true);
  
  try {
    // 모든 비동기 작업
    final data = await _handler.queryAll();
    
    // 명시적 조건 체크
    if (data.isEmpty) {
      setState(() {
        _dataList = [];
        _isLoading = false;
      });
      return;
    }
    
    setState(() {
      _dataList = data;
      _isLoading = false;
    });
  } catch (e, stackTrace) {
    // 에러 로깅 및 상태 복구
    AppLogger.e('데이터 로드 실패', error: e, stackTrace: stackTrace);
    setState(() {
      _dataList = [];
      _isLoading = false;
    });
  }
}
```

---

## 핸들러 사용 패턴

### 핸들러 선언

```dart
// ✅ 좋은 예: 클래스 필드로 선언
class _MyScreenState extends State<MyScreen> {
  final PurchaseHandler _purchaseHandler = PurchaseHandler();
  final PurchaseItemHandler _purchaseItemHandler = PurchaseItemHandler();
  
  // 사용
  Future<void> _loadData() async {
    final orders = await _purchaseHandler.queryAll();
  }
}
```

### 서비스 활용 (복합 쿼리)

```dart
// ✅ 좋은 예: 복잡한 조인 쿼리는 서비스 사용
final purchaseService = PurchaseService();
final orderDetail = await purchaseService.queryOrderListWithItems(purchaseId);
```

---

## 체크리스트

화면 구현 시 확인 사항:

- [ ] 핸들러는 클래스 필드로 선언했는가?
- [ ] 데이터 로드는 initState에서 시작하는가?
- [ ] try-catch는 최상위 레벨에만 있는가?
- [ ] null 체크는 명시적으로 하는가?
- [ ] 유틸리티 함수를 활용하는가? (OrderStatusUtils 등)
- [ ] Map을 활용해 데이터를 효율적으로 캐싱하는가?
- [ ] setState는 최소한으로 호출하는가?
- [ ] 에러 발생 시 상태를 안전하게 복구하는가?

---

## 요약

1. **단순성**: 복잡한 로직은 유틸리티로 분리
2. **효율성**: Map 활용, 불필요한 조회 최소화
3. **일관성**: 모든 화면에서 동일한 패턴 사용
4. **명시성**: null 체크, 조건 분기를 명확하게
5. **안정성**: 에러 발생 시 상태 안전하게 복구
