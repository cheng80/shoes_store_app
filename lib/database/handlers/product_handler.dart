import 'package:shoes_store_app/config.dart' as config;
import 'package:shoes_store_app/database/core/database_manager.dart';
import 'package:shoes_store_app/model/product/product.dart';
import 'package:sqflite/sqflite.dart';

/// Product 테이블 핸들러
/// 
/// Product 테이블의 모든 CRUD 작업 및 조인 쿼리를 담당합니다.
/// Product는 ProductBase와 Manufacturer를 참조하는 중간 테이블입니다.
class ProductHandler {
  /// DatabaseManager 인스턴스
  final DatabaseManager _dbManager = DatabaseManager();

  /// DB 인스턴스 가져오기
  Future<Database> _getDatabase() async {
    return await _dbManager.getDatabase();
  }

  // ============================================
  // 기본 조회 메서드
  // ============================================

  /// 전체 제품 조회
  /// 
  /// 반환: 모든 Product 리스트
  Future<List<Product>> queryAll() async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableProduct,
      orderBy: 'id ASC',
    );
    return results.map((e) => Product.fromMap(e)).toList();
  }

  /// ID로 제품 조회
  /// 
  /// [id] Product ID
  /// 반환: Product 객체 (없으면 null)
  Future<Product?> queryById(int id) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableProduct,
      where: 'id = ?',
      whereArgs: [id],
      limit: 1,
    );
    if (results.isEmpty) return null;
    return Product.fromMap(results.first);
  }

  /// ProductBase별 제품 조회
  /// 
  /// [pbid] ProductBase ID
  /// 반환: 해당 ProductBase의 모든 사이즈/재고 정보를 가진 Product 리스트
  Future<List<Product>> queryByProductBaseId(int pbid) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableProduct,
      where: 'pbid = ?',
      whereArgs: [pbid],
      orderBy: 'size ASC',
    );
    return results.map((e) => Product.fromMap(e)).toList();
  }

  /// 제조사별 제품 조회
  /// 
  /// [mfid] Manufacturer ID
  /// 반환: 해당 제조사의 모든 Product 리스트
  Future<List<Product>> queryByManufacturerId(int mfid) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableProduct,
      where: 'mfid = ?',
      whereArgs: [mfid],
      orderBy: 'id ASC',
    );
    return results.map((e) => Product.fromMap(e)).toList();
  }

  /// 사이즈별 제품 조회
  /// 
  /// [size] 제품 사이즈 (220, 230, 240 등)
  /// 반환: 해당 사이즈의 모든 Product 리스트
  Future<List<Product>> queryBySize(int size) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableProduct,
      where: 'size = ?',
      whereArgs: [size],
      orderBy: 'id ASC',
    );
    return results.map((e) => Product.fromMap(e)).toList();
  }

  // ============================================
  // 조인 쿼리 메서드
  // ============================================

  /// 제품 + ProductBase 정보 조인 조회
  /// 
  /// [id] Product ID
  /// 반환: Product와 ProductBase 정보를 포함한 Map
  /// 
  /// 사용 예시:
  /// ```dart
  /// final handler = ProductHandler();
  /// final productWithBase = await handler.queryWithBase(productId);
  /// print(productWithBase['pName']); // 제품명
  /// print(productWithBase['pColor']); // 색상
  /// ```
  Future<Map<String, dynamic>?> queryWithBase(int id) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.rawQuery('''
      SELECT 
        Product.*,
        ProductBase.pName,
        ProductBase.pDescription,
        ProductBase.pColor,
        ProductBase.pGender,
        ProductBase.pStatus,
        ProductBase.pCategory,
        ProductBase.pModelNumber
      FROM Product
      JOIN ProductBase ON Product.pbid = ProductBase.id
      WHERE Product.id = ?
    ''', [id]);

    if (results.isEmpty) return null;
    return Map<String, dynamic>.from(results.first);
  }

  /// 제품 + ProductBase + Manufacturer 정보 조인 조회
  /// 
  /// [id] Product ID
  /// 반환: Product, ProductBase, Manufacturer 정보를 모두 포함한 Map
  /// 
  /// 사용 예시:
  /// ```dart
  /// final handler = ProductHandler();
  /// final fullInfo = await handler.queryWithBaseAndManufacturer(productId);
  /// print(fullInfo['mName']); // 제조사명 (예: '나이키', '뉴발란스')
  /// print(fullInfo['pName']); // 제품명
  /// print(fullInfo['size']); // 사이즈
  /// ```
  Future<Map<String, dynamic>?> queryWithBaseAndManufacturer(int id) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.rawQuery('''
      SELECT 
        Product.*,
        ProductBase.pName,
        ProductBase.pDescription,
        ProductBase.pColor,
        ProductBase.pGender,
        ProductBase.pStatus,
        ProductBase.pCategory,
        ProductBase.pModelNumber,
        Manufacturer.mName
      FROM Product
      JOIN ProductBase ON Product.pbid = ProductBase.id
      JOIN Manufacturer ON Product.mfid = Manufacturer.id
      WHERE Product.id = ?
    ''', [id]);

    if (results.isEmpty) return null;
    return Map<String, dynamic>.from(results.first);
  }

  /// ProductBase별 제품 목록 + ProductBase 정보 조인 조회
  /// 
  /// [pbid] ProductBase ID
  /// 반환: 해당 ProductBase의 모든 사이즈별 제품 정보를 포함한 Map 리스트
  /// 
  /// 사용 예시:
  /// ```dart
  /// final handler = ProductHandler();
  /// final products = await handler.queryListWithBase(productBaseId);
  /// // products에는 각 사이즈별 제품 정보가 포함됨
  /// for (var product in products) {
  ///   print('${product['pName']} - 사이즈: ${product['size']}, 재고: ${product['pQuantity']}');
  /// }
  /// ```
  Future<List<Map<String, dynamic>>> queryListWithBase(int pbid) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.rawQuery('''
      SELECT 
        Product.*,
        ProductBase.pName,
        ProductBase.pDescription,
        ProductBase.pColor,
        ProductBase.pGender,
        ProductBase.pStatus,
        ProductBase.pCategory,
        ProductBase.pModelNumber
      FROM Product
      JOIN ProductBase ON Product.pbid = ProductBase.id
      WHERE Product.pbid = ?
      ORDER BY Product.size ASC
    ''', [pbid]);

    return results.map((e) => Map<String, dynamic>.from(e)).toList();
  }

  // ============================================
  // 삽입 메서드
  // ============================================

  /// 제품 추가
  /// 
  /// [product] 추가할 Product 객체
  /// 반환: 삽입된 레코드의 ID
  Future<int> insertData(Product product) async {
    final db = await _getDatabase();
    final map = product.toMap(includeId: false);
    return await db.insert(config.kTableProduct, map);
  }

  // ============================================
  // 수정 메서드
  // ============================================

  /// 제품 정보 수정
  /// 
  /// [product] 수정할 Product 객체 (id 필수)
  /// 반환: 업데이트된 행 수
  Future<int> updateData(Product product) async {
    if (product.id == null) {
      throw Exception('Product id is null. Cannot update.');
    }

    final db = await _getDatabase();
    final map = product.toMap(includeId: false);
    return await db.update(
      config.kTableProduct,
      map,
      where: 'id = ?',
      whereArgs: [product.id],
    );
  }

  /// 제품 재고만 업데이트
  /// 
  /// [id] Product ID
  /// [quantity] 새로운 재고 수량
  /// 반환: 업데이트된 행 수
  /// 
  /// 사용 예시:
  /// ```dart
  /// final handler = ProductHandler();
  /// await handler.updateQuantity(productId, 100); // 재고를 100으로 변경
  /// ```
  Future<int> updateQuantity(int id, int quantity) async {
    final db = await _getDatabase();
    return await db.update(
      config.kTableProduct,
      {'pQuantity': quantity},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  // ============================================
  // 삭제 메서드
  // ============================================

  /// 제품 삭제
  /// 
  /// [id] 삭제할 Product ID
  /// 반환: 삭제된 행 수
  /// 
  /// 주의: PurchaseItem에서 참조 중인 제품은 삭제하지 않는 것이 좋습니다.
  Future<int> deleteData(int id) async {
    final db = await _getDatabase();
    return await db.delete(
      config.kTableProduct,
      where: 'id = ?',
      whereArgs: [id],
    );
  }
}

