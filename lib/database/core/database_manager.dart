import 'package:shoes_store_app/config.dart' as config;
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

/// SQLite 데이터베이스 초기화 및 관리 클래스
/// 
/// 모든 테이블 생성 및 인덱스 관리를 담당합니다.
class DatabaseManager {
  /// DB 인스턴스 (싱글톤 패턴)
  static Database? _db;

  /// DB 초기화 및 테이블 생성
  /// 
  /// [dbName] 데이터베이스 파일명
  /// [dVersion] 데이터베이스 버전
  /// 반환: 초기화된 Database 인스턴스
  Future<Database> initializeDB() async {
    if (_db != null) return _db!;

    final String dbName = '${config.kDBName}${config.kDBFileExt}';
    final int dVersion = config.kVersion;

    final path = join(await getDatabasesPath(), dbName);
    print("Database Path: $path");

    _db = await openDatabase(
      path,
      version: dVersion,
      onCreate: (db, version) async {
        // 테이블 생성
        await _createTables(db);
        // 인덱스 생성
        await _createIndexes(db);
      },
    );

    return _db!;
  }

  /// 모든 테이블 생성
  /// 
  /// [db] Database 인스턴스
  Future<void> _createTables(Database db) async {
    // Product 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS Product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pbid INTEGER,
        mfid INTEGER,
        size INTEGER,
        basePrice INTEGER,
        pQuantity INTEGER
      )
    ''');

    // ProductBase 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS ProductBase (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pName TEXT,
        pDescription TEXT,
        pColor TEXT,
        pGender TEXT,
        pStatus TEXT,
        pFeatureType TEXT,
        pCategory TEXT,
        pModelNumber TEXT
      )
    ''');

    // Manufacturer 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS Manufacturer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mName TEXT
      )
    ''');

    // ProductImage 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS ProductImage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pbid INTEGER,
        imagePath TEXT
      )
    ''');

    // Customer 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS Customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cEmail TEXT,
        cPhoneNumber TEXT,
        cName TEXT,
        cPassword TEXT
      )
    ''');

    // Employee 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS Employee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eEmail TEXT,
        ePhoneNumber TEXT,
        eName TEXT,
        ePassword TEXT,
        eRole TEXT
      )
    ''');

    // PurchaseItem 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS PurchaseItem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pid INTEGER,
        pcid INTEGER,
        pcQuantity INTEGER,
        pcStatus TEXT
      )
    ''');

    // Purchase 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS Purchase (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cid INTEGER,
        pickupDate TEXT,
        orderCode TEXT,
        timeStamp TEXT
      )
    ''');

    // LoginHistory 테이블
    await db.execute('''
      CREATE TABLE IF NOT EXISTS LoginHistory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cid INTEGER,
        loginTime TEXT,
        lStatus TEXT,
        lVersion REAL,
        lAddress TEXT,
        lPaymentMethod TEXT
      )
    ''');
  }

  /// 인덱스 생성 (조인 쿼리 성능 향상)
  /// 
  /// [db] Database 인스턴스
  Future<void> _createIndexes(Database db) async {
    // Purchase 테이블 인덱스
    // 고객별 주문 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_purchase_cid 
      ON Purchase(cid)
    ''');

    // 주문 코드로 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_purchase_order_code 
      ON Purchase(orderCode)
    ''');

    // PurchaseItem 테이블 인덱스
    // 주문별 항목 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_purchase_item_pcid 
      ON PurchaseItem(pcid)
    ''');

    // 제품별 주문 항목 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_purchase_item_pid 
      ON PurchaseItem(pid)
    ''');

    // 상태별 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_purchase_item_status 
      ON PurchaseItem(pcStatus)
    ''');

    // Product 테이블 인덱스
    // ProductBase별 제품 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_product_pbid 
      ON Product(pbid)
    ''');

    // 제조사별 제품 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_product_mfid 
      ON Product(mfid)
    ''');

    // ProductImage 테이블 인덱스
    // ProductBase별 이미지 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_product_image_pbid 
      ON ProductImage(pbid)
    ''');

    // Customer 테이블 인덱스
    // 이메일로 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_customer_email 
      ON Customer(cEmail)
    ''');

    // 전화번호로 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_customer_phone 
      ON Customer(cPhoneNumber)
    ''');

    // Employee 테이블 인덱스
    // 이메일로 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_employee_email 
      ON Employee(eEmail)
    ''');

    // 전화번호로 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_employee_phone 
      ON Employee(ePhoneNumber)
    ''');

    // 역할별 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_employee_role 
      ON Employee(eRole)
    ''');

    // LoginHistory 테이블 인덱스
    // 고객별 로그인 이력 조회 최적화
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_login_history_cid 
      ON LoginHistory(cid)
    ''');

    print("✅ 모든 인덱스 생성 완료");
  }

  /// DB 인스턴스 가져오기 (다른 핸들러에서 사용)
  /// 
  /// 반환: Database 인스턴스
  Future<Database> getDatabase() async {
    if (_db == null) {
      await initializeDB();
    }
    return _db!;
  }

  /// DB 연결 닫기 및 리셋
  /// 
  /// DB를 삭제하거나 재초기화하기 전에 호출해야 합니다.
  /// 기존 연결을 안전하게 닫고 인스턴스를 리셋합니다.
  Future<void> closeAndReset() async {
    if (_db != null) {
      await _db!.close();
      _db = null;
    }
  }

  /// 테이블 전체 삭제 (개발/테스트용)
  Future<void> clearAllTables() async {
    final db = await getDatabase();
    await db.delete('LoginHistory');
    await db.delete('PurchaseItem');
    await db.delete('Purchase');
    await db.delete('Employee');
    await db.delete('Customer');
    await db.delete('ProductImage');
    await db.delete('Product');
    await db.delete('ProductBase');
    await db.delete('Manufacturer');
    print("✅ 모든 테이블 데이터 삭제 완료");
  }
}

