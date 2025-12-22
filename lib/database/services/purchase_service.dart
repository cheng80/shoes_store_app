import 'package:shoes_store_app/config.dart' as config;
import 'package:shoes_store_app/database/core/database_manager.dart';
import 'package:sqflite/sqflite.dart';

/// Purchase 관련 복합 조인 쿼리 서비스
/// 
/// 여러 테이블을 조인하여 주문 상세 정보를 조회하는 복잡한 쿼리를 담당합니다.
/// PurchaseHandler와 PurchaseItemHandler의 기본 기능을 조합하여 사용합니다.
class PurchaseService {
  /// DatabaseManager 인스턴스
  final DatabaseManager _dbManager = DatabaseManager();

  /// DB 인스턴스 가져오기
  Future<Database> _getDatabase() async {
    return await _dbManager.getDatabase();
  }

  // ============================================
  // 복합 조인 쿼리 메서드
  // ============================================

  /// 주문 상세 정보 조회 (전체 조인)
  /// 
  /// Purchase + PurchaseItem + Product + ProductBase + Manufacturer + Customer + 이미지
  /// 
  /// [purchaseId] Purchase ID
  /// 반환: 주문 정보, 고객 정보, 주문 항목 리스트를 포함한 Map
  /// 
  /// 반환 구조:
  /// ```dart
  /// {
  ///   'purchase': Purchase 정보,
  ///   'customer': Customer 정보,
  ///   'items': [
  ///     {
  ///       'purchaseItem': PurchaseItem 정보,
  ///       'product': Product 정보,
  ///       'productBase': ProductBase 정보,
  ///       'manufacturer': Manufacturer 정보,
  ///       'imagePath': 첫 번째 이미지 경로
  ///     },
  ///     ...
  ///   ]
  /// }
  /// ```
  /// 
  /// 사용 예시:
  /// ```dart
  /// final service = PurchaseService();
  /// final orderDetail = await service.queryOrderDetail(purchaseId);
  /// 
  /// final purchase = orderDetail['purchase'] as Map<String, dynamic>;
  /// final customer = orderDetail['customer'] as Map<String, dynamic>;
  /// final items = orderDetail['items'] as List<Map<String, dynamic>>;
  /// 
  /// print('주문 코드: ${purchase['orderCode']}');
  /// print('고객명: ${customer['cName']}');
  /// for (var item in items) {
  ///   print('제품명: ${item['productBase']['pName']}');
  ///   print('수량: ${item['purchaseItem']['pcQuantity']}');
  /// }
  /// ```
  Future<Map<String, dynamic>?> queryOrderDetail(int purchaseId) async {
    final db = await _getDatabase();

    // 1. Purchase + Customer 조인 조회
    final purchaseResults = await db.rawQuery('''
      SELECT 
        Purchase.*,
        Customer.cName,
        Customer.cEmail,
        Customer.cPhoneNumber
      FROM Purchase
      JOIN Customer ON Purchase.cid = Customer.id
      WHERE Purchase.id = ?
    ''', [purchaseId]);

    if (purchaseResults.isEmpty) return null;

    // 2. PurchaseItem + Product + ProductBase + Manufacturer + 이미지 조인 조회
    final itemResults = await db.rawQuery('''
      SELECT 
        PurchaseItem.*,
        Product.size,
        Product.basePrice,
        Product.pQuantity,
        ProductBase.pName,
        ProductBase.pDescription,
        ProductBase.pColor,
        ProductBase.pGender,
        ProductBase.pCategory,
        ProductBase.pModelNumber,
        Manufacturer.mName,
        (SELECT imagePath FROM ProductImage 
        WHERE ProductImage.pbid = ProductBase.id 
        LIMIT 1) as imagePath
      FROM PurchaseItem
      JOIN Product ON PurchaseItem.pid = Product.id
      JOIN ProductBase ON Product.pbid = ProductBase.id
      JOIN Manufacturer ON Product.mfid = Manufacturer.id
      WHERE PurchaseItem.pcid = ?
      ORDER BY PurchaseItem.id ASC
    ''', [purchaseId]);

    return {
      'purchase': Map<String, dynamic>.from(purchaseResults.first),
      'customer': {
        'cName': purchaseResults.first['cName'],
        'cEmail': purchaseResults.first['cEmail'],
        'cPhoneNumber': purchaseResults.first['cPhoneNumber'],
      },
      'items': itemResults.map((e) => {
        'purchaseItem': {
          'id': e['id'],
          'pid': e['pid'],
          'pcid': e['pcid'],
          'pcQuantity': e['pcQuantity'],
          'pcStatus': e['pcStatus'],
        },
        'product': {
          'id': e['pid'],
          'size': e['size'],
          'basePrice': e['basePrice'],
          'pQuantity': e['pQuantity'],
        },
        'productBase': {
          'pName': e['pName'],
          'pDescription': e['pDescription'],
          'pColor': e['pColor'],
          'pGender': e['pGender'],
          'pCategory': e['pCategory'],
          'pModelNumber': e['pModelNumber'],
        },
        'manufacturer': {
          'mName': e['mName'],
        },
        'imagePath': e['imagePath'],
      }).toList(),
    };
  }

  /// 고객별 주문 목록 조회 (전체 조인)
  /// 
  /// 고객의 모든 주문과 각 주문의 항목 수, 총 금액을 포함하여 조회합니다.
  /// 
  /// [cid] Customer ID
  /// 반환: 주문 목록과 각 주문의 요약 정보를 포함한 Map 리스트
  /// 
  /// 반환 구조:
  /// ```dart
  /// [
  ///   {
  ///     'purchase': Purchase 정보,
  ///     'itemCount': 주문 항목 수,
  ///     'totalPrice': 총 금액
  ///   },
  ///   ...
  /// ]
  /// ```
  /// 
  /// 사용 예시:
  /// ```dart
  /// final service = PurchaseService();
  /// final orders = await service.queryOrderListByCustomer(customerId);
  /// 
  /// for (var order in orders) {
  ///   print('주문 코드: ${order['purchase']['orderCode']}');
  ///   print('항목 수: ${order['itemCount']}');
  ///   print('총 금액: ${order['totalPrice']}원');
  /// }
  /// ```
  Future<List<Map<String, dynamic>>> queryOrderListByCustomer(int cid) async {
    final db = await _getDatabase();

    final results = await db.rawQuery('''
      SELECT 
        Purchase.*,
        COUNT(PurchaseItem.id) as itemCount,
        SUM(Product.basePrice * PurchaseItem.pcQuantity) as totalPrice
      FROM Purchase
      LEFT JOIN PurchaseItem ON Purchase.id = PurchaseItem.pcid
      LEFT JOIN Product ON PurchaseItem.pid = Product.id
      WHERE Purchase.cid = ?
      GROUP BY Purchase.id
      ORDER BY Purchase.timeStamp DESC
    ''', [cid]);

    return results.map((e) => {
      'purchase': {
        'id': e['id'],
        'cid': e['cid'],
        'pickupDate': e['pickupDate'],
        'orderCode': e['orderCode'],
        'timeStamp': e['timeStamp'],
      },
      'itemCount': e['itemCount'] ?? 0,
      'totalPrice': e['totalPrice'] ?? 0,
    }).toList();
  }

  /// 주문 + 모든 주문 항목 조인 조회
  /// 
  /// 주문 정보와 해당 주문의 모든 항목을 한 번에 조회합니다.
  /// 
  /// [purchaseId] Purchase ID
  /// 반환: 주문 정보와 주문 항목 리스트를 포함한 Map
  /// 
  /// 사용 예시:
  /// ```dart
  /// final service = PurchaseService();
  /// final orderWithItems = await service.queryOrderListWithItems(purchaseId);
  /// 
  /// final purchase = orderWithItems['purchase'] as Map<String, dynamic>;
  /// final items = orderWithItems['items'] as List<Map<String, dynamic>>;
  /// ```
  Future<Map<String, dynamic>?> queryOrderListWithItems(int purchaseId) async {
    final db = await _getDatabase();

    // Purchase 정보 조회
    final purchaseResults = await db.query(
      'Purchase',
      where: 'id = ?',
      whereArgs: [purchaseId],
      limit: 1,
    );

    if (purchaseResults.isEmpty) return null;

    // PurchaseItem + Product + ProductBase + Manufacturer 조인 조회
    final itemResults = await db.rawQuery('''
      SELECT 
        PurchaseItem.*,
        Product.size,
        Product.basePrice,
        Product.pQuantity,
        ProductBase.pName,
        ProductBase.pDescription,
        ProductBase.pColor,
        ProductBase.pGender,
        ProductBase.pCategory,
        ProductBase.pModelNumber,
        Manufacturer.mName
      FROM PurchaseItem
      JOIN Product ON PurchaseItem.pid = Product.id
      JOIN ProductBase ON Product.pbid = ProductBase.id
      JOIN Manufacturer ON Product.mfid = Manufacturer.id
      WHERE PurchaseItem.pcid = ?
      ORDER BY PurchaseItem.id ASC
    ''', [purchaseId]);

    return {
      'purchase': Map<String, dynamic>.from(purchaseResults.first),
      'items': itemResults.map((e) => Map<String, dynamic>.from(e)).toList(),
    };
  }

  /// 반품 가능한 주문 목록 조회
  /// 
  /// 주문 상태가 '제품 수령 완료'(status 2)이고 반품 신청이 되지 않은 주문만 조회합니다.
  /// config.pickupStatus의 한글 값과 숫자 문자열을 모두 지원합니다.
  /// 
  /// [cid] Customer ID
  /// 반환: 반품 가능한 주문 목록
  /// 
  /// 사용 예시:
  /// ```dart
  /// final service = PurchaseService();
  /// final returnableOrders = await service.queryReturnableOrders(customerId);
  /// // 반품 가능한 주문만 필터링되어 반환됨
  /// ```
  Future<List<Map<String, dynamic>>> queryReturnableOrders(int cid) async {
    final db = await _getDatabase();

    // config.pickupStatus의 한글 값 사용
    final completeStatus = config.pickupStatus[2] ?? '제품 수령 완료';
    final returnRequestStatus = config.pickupStatus[3] ?? '반품 신청';
    final returnDoneStatus = config.pickupStatus[5] ?? '반품 완료';

    final results = await db.rawQuery('''
      SELECT DISTINCT
        Purchase.*
      FROM Purchase
      JOIN PurchaseItem ON Purchase.id = PurchaseItem.pcid
      WHERE Purchase.cid = ?
        AND PurchaseItem.pcStatus = ?
        AND PurchaseItem.pcStatus != ?
        AND PurchaseItem.pcStatus != ?
      ORDER BY Purchase.timeStamp DESC
    ''', [cid, completeStatus, returnRequestStatus, returnDoneStatus]);

    return results.map((e) => Map<String, dynamic>.from(e)).toList();
  }
}

