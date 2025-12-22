import 'package:shoes_store_app/config.dart' as config;
import 'package:shoes_store_app/database/core/database_manager.dart';
import 'package:shoes_store_app/model/sale/retail.dart';
import 'package:sqflite/sqflite.dart';

/// Retail 테이블 핸들러
/// 
/// Retail 테이블의 모든 CRUD 작업을 담당합니다.
/// Retail은 대리점별 제품 재고를 관리하는 테이블입니다.
class RetailHandler {
  /// DatabaseManager 인스턴스
  final DatabaseManager _dbManager = DatabaseManager();

  /// DB 인스턴스 가져오기
  Future<Database> _getDatabase() async {
    return await _dbManager.getDatabase();
  }

  // ============================================
  // 조회 메서드
  // ============================================

  /// 전체 대리점 재고 조회
  /// 
  /// 반환: 모든 Retail 리스트
  Future<List<Retail>> queryAll() async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableRetail,
      orderBy: 'id ASC',
    );
    return results.map((e) => Retail.fromMap(e)).toList();
  }

  /// ID로 대리점 재고 조회
  /// 
  /// [id] Retail ID
  /// 반환: Retail 객체 (없으면 null)
  Future<Retail?> queryById(int id) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableRetail,
      where: 'id = ?',
      whereArgs: [id],
      limit: 1,
    );
    if (results.isEmpty) return null;
    return Retail.fromMap(results.first);
  }

  /// 제품별 재고 조회
  /// 
  /// [pid] Product ID
  /// 반환: 해당 제품의 모든 대리점 재고 리스트
  /// 
  /// 사용 예시:
  /// ```dart
  /// final handler = RetailHandler();
  /// final stocks = await handler.queryByProductId(productId);
  /// // stocks에는 해당 제품이 있는 모든 대리점의 재고 정보가 포함됨
  /// ```
  Future<List<Retail>> queryByProductId(int pid) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableRetail,
      where: 'pid = ?',
      whereArgs: [pid],
      orderBy: 'id ASC',
    );
    return results.map((e) => Retail.fromMap(e)).toList();
  }

  /// 직원(대리점)별 재고 조회
  /// 
  /// [eid] Employee ID (대리점장 ID)
  /// 반환: 해당 대리점의 모든 제품 재고 리스트
  /// 
  /// 사용 예시:
  /// ```dart
  /// final handler = RetailHandler();
  /// final stocks = await handler.queryByEmployeeId(employeeId);
  /// // stocks에는 해당 대리점의 모든 제품 재고 정보가 포함됨
  /// ```
  Future<List<Retail>> queryByEmployeeId(int eid) async {
    final db = await _getDatabase();
    final List<Map<String, Object?>> results = await db.query(
      config.kTableRetail,
      where: 'eid = ?',
      whereArgs: [eid],
      orderBy: 'id ASC',
    );
    return results.map((e) => Retail.fromMap(e)).toList();
  }

  // ============================================
  // 삽입 메서드
  // ============================================

  /// 대리점 재고 추가
  /// 
  /// [retail] 추가할 Retail 객체
  /// 반환: 삽입된 레코드의 ID
  Future<int> insertData(Retail retail) async {
    final db = await _getDatabase();
    final map = retail.toMap(includeId: false);
    return await db.insert(config.kTableRetail, map);
  }

  // ============================================
  // 수정 메서드
  // ============================================

  /// 대리점 재고 정보 수정
  /// 
  /// [retail] 수정할 Retail 객체 (id 필수)
  /// 반환: 업데이트된 행 수
  Future<int> updateData(Retail retail) async {
    if (retail.id == null) {
      throw Exception('Retail id is null. Cannot update.');
    }

    final db = await _getDatabase();
    final map = retail.toMap(includeId: false);
    return await db.update(
      config.kTableRetail,
      map,
      where: 'id = ?',
      whereArgs: [retail.id],
    );
  }

  /// 대리점 재고 수량만 업데이트
  /// 
  /// [id] Retail ID
  /// [quantity] 새로운 재고 수량
  /// 반환: 업데이트된 행 수
  /// 
  /// 사용 예시:
  /// ```dart
  /// final handler = RetailHandler();
  /// await handler.updateQuantity(retailId, 50); // 재고를 50으로 변경
  /// ```
  Future<int> updateQuantity(int id, int quantity) async {
    final db = await _getDatabase();
    return await db.update(
      config.kTableRetail,
      {'rQuantity': quantity},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  // ============================================
  // 삭제 메서드
  // ============================================

  /// 대리점 재고 삭제
  /// 
  /// [id] 삭제할 Retail ID
  /// 반환: 삭제된 행 수
  Future<int> deleteData(int id) async {
    final db = await _getDatabase();
    return await db.delete(
      config.kTableRetail,
      where: 'id = ?',
      whereArgs: [id],
    );
  }
}

