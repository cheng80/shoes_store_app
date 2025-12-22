# db.query vs db.rawQuery 비교 가이드

**작성일**: 2025-12-17  
**목적**: SQLite/SQFlite에서 `db.query`와 `db.rawQuery`의 차이점과 사용 시나리오 설명

---

## 📋 요약

| 항목 | `db.query` | `db.rawQuery` |
|------|-----------|---------------|
| **쿼리 작성 방식** | 구조화된 파라미터 | 원시 SQL 문자열 |
| **사용 복잡도** | 간단 | 복잡 |
| **적용 케이스** | 단일 테이블 조회 | 조인, 복잡한 쿼리 |
| **SQL Injection 방지** | 자동 처리 | 수동 처리 필요 |
| **가독성** | 높음 | 중간 |
| **유연성** | 제한적 | 매우 높음 |

---

## 🔍 상세 비교

### 1. db.query (구조화된 쿼리)

**특징**:
- 구조화된 파라미터로 쿼리 구성
- SQL Injection 방지가 자동으로 처리됨
- 단일 테이블 조회에 최적화
- 컴파일 타임에 구문 검사 가능

**문법**:
```dart
Future<List<Map<String, Object?>>> query(
  String table, {
  bool? distinct,
  List<String>? columns,
  String? where,
  List<Object?>? whereArgs,
  String? groupBy,
  String? having,
  String? orderBy,
  int? limit,
  int? offset,
})
```

**실제 사용 예시** (CustomerHandler에서):

```dart
// 예제 1: 전체 조회
Future<List<Customer>> queryAll() async {
  final db = await _getDatabase();
  final results = await db.query(
    config.kTableCustomer,  // 테이블명
    orderBy: 'id ASC',       // 정렬
  );
  return results.map((e) => Customer.fromMap(e)).toList();
}

// 예제 2: 조건부 조회
Future<Customer?> queryById(int id) async {
  final db = await _getDatabase();
  final results = await db.query(
    config.kTableCustomer,  // 테이블명
    where: 'id = ?',        // WHERE 조건
    whereArgs: [id],        // ? 플레이스홀더 값
    limit: 1,               // 최대 1개만 조회
  );
  if (results.isEmpty) return null;
  return Customer.fromMap(results.first);
}

// 예제 3: 이메일로 조회
Future<Customer?> queryByEmail(String email) async {
  final db = await _getDatabase();
  final results = await db.query(
    config.kTableCustomer,
    where: 'cEmail = ?',    // WHERE 조건
    whereArgs: [email],     // SQL Injection 방지를 위해 ? 사용
    limit: 1,
  );
  if (results.isEmpty) return null;
  return Customer.fromMap(results.first);
}

// 예제 4: 여러 컬럼 선택
final results = await db.query(
  'Customer',
  columns: ['id', 'cName', 'cEmail'],  // 특정 컬럼만 선택
  where: 'cEmail = ?',
  whereArgs: [email],
);

// 예제 5: 정렬 및 제한
final results = await db.query(
  'Purchase',
  where: 'cid = ?',
  whereArgs: [customerId],
  orderBy: 'timeStamp DESC',  // 최신순 정렬
  limit: 10,                  // 최대 10개만
);
```

**장점**:
- ✅ SQL Injection 자동 방지 (`?` 플레이스홀더 사용)
- ✅ 코드 가독성 좋음
- ✅ 타입 안정성 (파라미터 검증)
- ✅ 실수 방지 (구문 오류 가능성 낮음)

**단점**:
- ❌ 조인 쿼리 불가능
- ❌ 복잡한 서브쿼리 불가능
- ❌ UNION, GROUP_CONCAT 등 고급 기능 제한

---

### 2. db.rawQuery (원시 SQL 쿼리)

**특징**:
- 완전한 SQL 문자열을 직접 작성
- 모든 SQL 기능 사용 가능 (JOIN, 서브쿼리, UNION 등)
- 복잡한 쿼리에 최적화
- SQL Injection 방지를 위해 `?` 플레이스홀더 수동 사용 필요

**문법**:
```dart
Future<List<Map<String, Object?>>> rawQuery(
  String sql,
  [List<Object?>? arguments]
)
```

**실제 사용 예시** (PurchaseHandler에서):

```dart
// 예제 1: 간단한 조인 (Purchase + Customer)
Future<Map<String, dynamic>?> queryWithCustomer(int id) async {
  final db = await _getDatabase();
  final results = await db.rawQuery('''
    SELECT 
      Purchase.*,
      Customer.cName,
      Customer.cEmail,
      Customer.cPhoneNumber
    FROM Purchase
    JOIN Customer ON Purchase.cid = Customer.id
    WHERE Purchase.id = ?
  ''', [id]);  // ? 플레이스홀더에 id 값 삽입
  
  if (results.isEmpty) return null;
  return Map<String, dynamic>.from(results.first);
}

// 예제 2: 복잡한 조인 (여러 테이블)
Future<List<Map<String, dynamic>>> queryListWithCustomer(int cid) async {
  final db = await _getDatabase();
  final results = await db.rawQuery('''
    SELECT 
      Purchase.*,
      Customer.cName,
      Customer.cEmail,
      Customer.cPhoneNumber
    FROM Purchase
    JOIN Customer ON Purchase.cid = Customer.id
    WHERE Purchase.cid = ?
    ORDER BY Purchase.timeStamp DESC
  ''', [cid]);
  
  return results.map((e) => Map<String, dynamic>.from(e)).toList();
}

// 예제 3: 서브쿼리 사용 (ProductBaseHandler에서)
Future<List<Map<String, dynamic>>> queryListWithFirstImage() async {
  final db = await _getDatabase();
  final results = await db.rawQuery('''
    SELECT 
      ProductBase.*,
      (SELECT imagePath FROM ProductImage 
       WHERE ProductImage.pbid = ProductBase.id 
       LIMIT 1) as firstImage
    FROM ProductBase
    ORDER BY ProductBase.id ASC
  ''');  // 서브쿼리 사용
  
  return results.map((e) => Map<String, dynamic>.from(e)).toList();
}

// 예제 4: 복잡한 조인 (ProductHandler에서)
Future<List<Map<String, dynamic>>> queryListWithBase(int pbid) async {
  final db = await _getDatabase();
  final results = await db.rawQuery('''
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
```

**장점**:
- ✅ 모든 SQL 기능 사용 가능 (JOIN, 서브쿼리, UNION 등)
- ✅ 매우 유연하고 강력함
- ✅ 복잡한 쿼리 작성 가능

**단점**:
- ❌ SQL Injection 위험 (부적절한 사용 시)
- ❌ 문자열이므로 컴파일 타임 검사 불가
- ❌ 실수 가능성 높음 (오타, 구문 오류)
- ❌ 코드 가독성 낮을 수 있음 (복잡한 쿼리)

---

## 🎯 사용 가이드라인

### ✅ db.query 사용 권장 상황

1. **단일 테이블 조회**
   ```dart
   // ✅ 권장
   final customers = await db.query(
     'Customer',
     where: 'id = ?',
     whereArgs: [id],
   );
   
   // ❌ 비권장 (rawQuery 사용 불필요)
   final customers = await db.rawQuery(
     'SELECT * FROM Customer WHERE id = ?',
     [id],
   );
   ```

2. **간단한 조건부 조회**
   ```dart
   // ✅ 권장
   final customers = await db.query(
     'Customer',
     where: 'cEmail = ? AND cStatus = ?',
     whereArgs: [email, 'active'],
     orderBy: 'cName ASC',
     limit: 10,
   );
   ```

3. **특정 컬럼만 선택**
   ```dart
   // ✅ 권장
   final results = await db.query(
     'Customer',
     columns: ['id', 'cName', 'cEmail'],  // 필요한 컬럼만
   );
   ```

### ✅ db.rawQuery 사용 권장 상황

1. **조인 쿼리 필요 시**
   ```dart
   // ✅ 필수 (db.query로는 불가능)
   final results = await db.rawQuery('''
     SELECT 
       Purchase.*,
       Customer.cName,
       Customer.cEmail
     FROM Purchase
     JOIN Customer ON Purchase.cid = Customer.id
     WHERE Purchase.id = ?
   ''', [purchaseId]);
   ```

2. **서브쿼리 필요 시**
   ```dart
   // ✅ 필수 (db.query로는 불가능)
   final results = await db.rawQuery('''
     SELECT 
       ProductBase.*,
       (SELECT COUNT(*) FROM Product 
        WHERE Product.pbid = ProductBase.id) as productCount
     FROM ProductBase
   ''');
   ```

3. **복잡한 집계 함수 사용**
   ```dart
   // ✅ rawQuery가 더 적합
   final results = await db.rawQuery('''
     SELECT 
       cid,
       COUNT(*) as orderCount,
       SUM(totalPrice) as totalAmount
     FROM Purchase
     GROUP BY cid
     HAVING COUNT(*) > 5
   ''');
   ```

---

## ⚠️ SQL Injection 방지

### ✅ 안전한 사용

```dart
// ✅ db.query: 자동으로 안전 (권장)
final results = await db.query(
  'Customer',
  where: 'cEmail = ?',    // ? 플레이스홀더 사용
  whereArgs: [email],     // 값은 whereArgs로 전달
);

// ✅ db.rawQuery: ? 플레이스홀더 사용 (권장)
final results = await db.rawQuery(
  'SELECT * FROM Customer WHERE cEmail = ?',
  [email],  // 값은 두 번째 파라미터로 전달
);
```

### ❌ 위험한 사용 (절대 금지!)

```dart
// ❌ 매우 위험! SQL Injection 취약점
final results = await db.rawQuery(
  "SELECT * FROM Customer WHERE cEmail = '$email'",  // 직접 문자열 삽입
);

// ❌ 매우 위험!
final email = "test@example.com' OR '1'='1";
// 결과: SELECT * FROM Customer WHERE cEmail = 'test@example.com' OR '1'='1'
// 모든 레코드가 조회됨!
```

**원칙**: 
- **절대로** 사용자 입력을 SQL 문자열에 직접 삽입하지 마세요
- **항상** `?` 플레이스홀더와 `whereArgs` 또는 `arguments` 파라미터를 사용하세요

---

## 🔄 프로젝트 내 사용 패턴

### 패턴 1: 기본 CRUD는 `db.query` 사용

```dart
// CustomerHandler, PurchaseHandler 등에서
Future<Customer?> queryById(int id) async {
  final db = await _getDatabase();
  final results = await db.query(  // ✅ db.query 사용
    config.kTableCustomer,
    where: 'id = ?',
    whereArgs: [id],
    limit: 1,
  );
  if (results.isEmpty) return null;
  return Customer.fromMap(results.first);
}
```

### 패턴 2: 조인 쿼리는 `db.rawQuery` 사용

```dart
// PurchaseHandler의 조인 메서드
Future<Map<String, dynamic>?> queryWithCustomer(int id) async {
  final db = await _getDatabase();
  final results = await db.rawQuery('''  // ✅ db.rawQuery 사용
    SELECT 
      Purchase.*,
      Customer.cName,
      Customer.cEmail
    FROM Purchase
    JOIN Customer ON Purchase.cid = Customer.id
    WHERE Purchase.id = ?
  ''', [id]);
  
  if (results.isEmpty) return null;
  return Map<String, dynamic>.from(results.first);
}
```

### 패턴 3: 복잡한 조인은 PurchaseService 사용

```dart
// PurchaseService에서 여러 테이블 조인
final results = await db.rawQuery('''
  SELECT 
    Purchase.*,
    Customer.*,
    PurchaseItem.*,
    Product.*,
    ProductBase.*,
    Manufacturer.*
  FROM Purchase
  JOIN Customer ON Purchase.cid = Customer.id
  JOIN PurchaseItem ON Purchase.id = PurchaseItem.pcid
  JOIN Product ON PurchaseItem.pid = Product.id
  JOIN ProductBase ON Product.pbid = ProductBase.id
  JOIN Manufacturer ON Product.mfid = Manufacturer.id
  WHERE Purchase.id = ?
''', [purchaseId]);
```

---

## 📊 비교 예제

### 같은 결과를 얻는 두 가지 방법

#### 목표: Customer ID가 1인 고객의 이메일 조회

**방법 1: db.query 사용**
```dart
final results = await db.query(
  'Customer',
  columns: ['cEmail'],     // 필요한 컬럼만 선택
  where: 'id = ?',
  whereArgs: [1],
  limit: 1,
);

final email = results.first['cEmail'] as String;
```

**방법 2: db.rawQuery 사용**
```dart
final results = await db.rawQuery(
  'SELECT cEmail FROM Customer WHERE id = ?',
  [1],
);

final email = results.first['cEmail'] as String;
```

**결론**: 이 경우 `db.query`가 더 명확하고 안전합니다.

---

#### 목표: 주문 정보와 고객 정보를 함께 조회

**방법 1: db.query 사용**
```dart
// ❌ 불가능! db.query는 조인을 지원하지 않음
// 두 번의 쿼리 필요:
final purchaseResults = await db.query('Purchase', where: 'id = ?', whereArgs: [id]);
final customerResults = await db.query('Customer', where: 'id = ?', whereArgs: [purchase.cid]);
// 그리고 수동으로 결합...
```

**방법 2: db.rawQuery 사용**
```dart
// ✅ 한 번의 쿼리로 해결
final results = await db.rawQuery('''
  SELECT 
    Purchase.*,
    Customer.cName,
    Customer.cEmail
  FROM Purchase
  JOIN Customer ON Purchase.cid = Customer.id
  WHERE Purchase.id = ?
''', [id]);

// 결과는 이미 결합되어 있음
```

**결론**: 조인 쿼리에는 `db.rawQuery`가 필수입니다.

---

## 💡 베스트 프랙티스

### 1. 우선순위

```
1순위: db.query (단순 조회)
2순위: db.rawQuery (조인 필요 시)
3순위: PurchaseService (복잡한 다중 조인)
```

### 2. 코드 구조

```dart
class CustomerHandler {
  // 기본 조회는 db.query 사용
  Future<List<Customer>> queryAll() async {
    final results = await db.query('Customer', orderBy: 'id ASC');
    // ...
  }
  
  // 조인이 필요한 경우에만 rawQuery 사용
  Future<Map<String, dynamic>?> queryWithOrders(int id) async {
    final results = await db.rawQuery('''
      SELECT Customer.*, COUNT(Purchase.id) as orderCount
      FROM Customer
      LEFT JOIN Purchase ON Customer.id = Purchase.cid
      WHERE Customer.id = ?
      GROUP BY Customer.id
    ''', [id]);
    // ...
  }
}
```

### 3. 주석 및 문서화

```dart
/// 고객별 주문 목록 + 고객 정보 조인 조회
/// 
/// [cid] Customer ID
/// 반환: Purchase와 Customer 정보를 포함한 Map 리스트
/// 
/// 주의: 조인이 필요하므로 rawQuery를 사용합니다.
Future<List<Map<String, dynamic>>> queryListWithCustomer(int cid) async {
  final db = await _getDatabase();
  final results = await db.rawQuery('''
    SELECT 
      Purchase.*,
      Customer.cName,
      Customer.cEmail,
      Customer.cPhoneNumber
    FROM Purchase
    JOIN Customer ON Purchase.cid = Customer.id
    WHERE Purchase.cid = ?
    ORDER BY Purchase.timeStamp DESC
  ''', [cid]);
  
  return results.map((e) => Map<String, dynamic>.from(e)).toList();
}
```

---

## ✅ 요약

### 언제 `db.query`를 사용할까?

- ✅ 단일 테이블 조회
- ✅ 간단한 WHERE 조건
- ✅ ORDER BY, LIMIT 사용
- ✅ 특정 컬럼만 선택
- ✅ 안전성과 가독성이 중요할 때

### 언제 `db.rawQuery`를 사용할까?

- ✅ 조인(JOIN) 쿼리 필요
- ✅ 서브쿼리 사용
- ✅ 복잡한 집계 함수
- ✅ UNION, GROUP BY 등 고급 기능
- ✅ `db.query`로 표현 불가능한 쿼리

### 핵심 원칙

1. **가능하면 `db.query` 사용** (더 안전하고 명확함)
2. **조인이 필요할 때만 `db.rawQuery` 사용**
3. **항상 `?` 플레이스홀더 사용** (SQL Injection 방지)
4. **복잡한 쿼리는 Service 레이어로 분리**

---

**문서 버전**: 1.0  
**최종 수정일**: 2025-12-17

