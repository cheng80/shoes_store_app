# 데이터베이스 마이그레이션 계획

**작성일**: 2025-12-17  
**목적**: SQLite → MySQL, 로컬 DB → FastAPI 백엔드 마이그레이션 계획  
**브랜치**: `dev`

---

## 📋 목차

1. [개요](#개요)
2. [마이그레이션 목표](#마이그레이션-목표)
3. [현재 구조 분석](#현재-구조-분석)
4. [마이그레이션 전략](#마이그레이션-전략)
5. [구조 설계](#구조-설계)
6. [단계별 구현 계획](#단계별-구현-계획)
7. [API 스펙 설계](#api-스펙-설계)
8. [데이터 마이그레이션](#데이터-마이그레이션)
9. [테스트 전략](#테스트-전략)
10. [롤백 계획](#롤백-계획)

---

## 개요

### 현재 상태
- **데이터베이스**: SQLite (로컬 파일)
- **접근 방식**: 직접 DB 접근 (sqflite)
- **구조**: DatabaseManager (싱글톤) → Handler (CRUD) → Service (복합 쿼리)

### 목표 상태
- **데이터베이스**: MySQL (서버)
- **접근 방식**: FastAPI 백엔드 (HTTP/JSON)
- **구조**: 기존 Handler 구조 최대한 유지, API 클라이언트 레이어 추가

---

## 마이그레이션 목표

### 핵심 원칙
1. **기존 핸들러 로직 최대한 재활용**
   - Handler 클래스의 메서드 시그니처 유지
   - 비즈니스 로직 변경 최소화
   - 모델 클래스 재사용

2. **구조 최소 변경**
   - Handler 인터페이스는 유지
   - 내부 구현만 변경 (SQLite → API 호출)
   - Service 레이어는 그대로 유지

3. **점진적 마이그레이션**
   - 단계별 구현 및 테스트
   - 기존 코드와 병행 운영 가능
   - 롤백 가능한 구조

---

## 현재 구조 분석

### 핵심 컴포넌트

#### 1. DatabaseManager
```dart
class DatabaseManager {
  static Database? _db;  // SQLite 인스턴스
  Future<Database> initializeDB() async { ... }
  Future<Database> getDatabase() async { ... }
}
```
- **역할**: SQLite DB 초기화 및 인스턴스 관리
- **변경 필요**: 추상화하여 SQLite/API 모두 지원

#### 2. Handler (예: CustomerHandler)
```dart
class CustomerHandler {
  final DatabaseManager _dbManager = DatabaseManager();
  
  Future<Database> _getDatabase() async {
    return await _dbManager.getDatabase();
  }
  
  Future<List<Customer>> queryAll() async {
    final db = await _getDatabase();
    final results = await db.query(config.kTableCustomer);
    return results.map((e) => Customer.fromMap(e)).toList();
  }
}
```
- **역할**: 테이블별 CRUD 작업
- **변경 필요**: DB 접근을 API 호출로 변경

#### 3. Service (예: PurchaseService)
```dart
class PurchaseService {
  final PurchaseHandler _purchaseHandler = PurchaseHandler();
  final PurchaseItemHandler _purchaseItemHandler = PurchaseItemHandler();
  // 복합 조인 쿼리
}
```
- **역할**: 복합 쿼리 및 비즈니스 로직
- **변경 필요**: 최소 (Handler만 교체)

---

## 마이그레이션 전략

### 전략: 추상화 레이어 도입

```
기존: Handler → DatabaseManager → SQLite
변경: Handler → DatabaseAdapter → [SQLite | API Client]
```

### 핵심 아이디어
1. **DatabaseAdapter 인터페이스** 생성
   - `query()`, `insert()`, `update()`, `delete()` 등 공통 메서드
   - SQLite 구현체와 API 구현체 제공

2. **Handler는 DatabaseAdapter 사용**
   - 기존 로직 유지
   - `_getDatabase()` → `_getAdapter()`로 변경
   - 내부 구현만 변경

3. **API Client 레이어**
   - FastAPI 엔드포인트 호출
   - JSON ↔ Dart 모델 변환
   - 에러 처리 및 재시도 로직

---

## 구조 설계

### 새로운 디렉토리 구조

```
lib/database/
├── core/
│   ├── database_manager.dart          # 기존 (SQLite용)
│   ├── database_adapter.dart          # NEW: 인터페이스
│   ├── sqlite_adapter.dart            # NEW: SQLite 구현
│   └── api_adapter.dart               # NEW: API 구현
│
├── api/                               # NEW: API 클라이언트
│   ├── api_client.dart                # HTTP 클라이언트
│   ├── endpoints.dart                 # API 엔드포인트 정의
│   ├── models/                        # API 요청/응답 모델
│   │   ├── api_request.dart
│   │   └── api_response.dart
│   └── services/                      # API 서비스별 클라이언트
│       ├── customer_api_service.dart
│       ├── product_api_service.dart
│       └── purchase_api_service.dart
│
├── handlers/                          # 기존 (최소 변경)
│   ├── customer_handler.dart          # DatabaseAdapter 사용
│   ├── product_handler.dart
│   └── ...
│
└── services/                          # 기존 (변경 없음)
    └── purchase_service.dart
```

---

## 단계별 구현 계획

### Phase 1: 추상화 레이어 구축

#### 1.1 DatabaseAdapter 인터페이스 정의
```dart
abstract class DatabaseAdapter {
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
  });
  
  Future<int> insert(String table, Map<String, Object?> values);
  Future<int> update(String table, Map<String, Object?> values, {String? where, List<Object?>? whereArgs});
  Future<int> delete(String table, {String? where, List<Object?>? whereArgs});
  Future<List<Map<String, Object?>>> rawQuery(String sql, [List<Object?>? arguments]);
}
```

#### 1.2 SQLiteAdapter 구현
```dart
class SQLiteAdapter implements DatabaseAdapter {
  final DatabaseManager _dbManager = DatabaseManager();
  
  Future<Database> _getDatabase() async {
    return await _dbManager.getDatabase();
  }
  
  @override
  Future<List<Map<String, Object?>>> query(...) async {
    final db = await _getDatabase();
    return await db.query(...);
  }
  // 기존 DatabaseManager 로직 재사용
}
```

#### 1.3 APIAdapter 구현 (스켈레톤)
```dart
class APIAdapter implements DatabaseAdapter {
  final ApiClient _apiClient = ApiClient();
  
  @override
  Future<List<Map<String, Object?>>> query(...) async {
    // API 호출로 변환
    final response = await _apiClient.get('/api/table/$table', queryParams: {...});
    return response.data;
  }
}
```

### Phase 2: API 클라이언트 구축

#### 2.1 ApiClient 기본 구조 (GET 전용)
```dart
class ApiClient {
  final String baseUrl;
  final Dio _dio = Dio();
  
  ApiClient({required this.baseUrl}) {
    _dio.options.baseUrl = baseUrl;
    _dio.options.connectTimeout = Duration(seconds: 10);
    _dio.options.receiveTimeout = Duration(seconds: 10);
    _setupInterceptors();
  }
  
  // GET 방식만 사용 (1단계)
  Future<Response> get(String path, {Map<String, dynamic>? queryParams});
  
  // 차후 구현 예정 (2단계)
  // Future<Response> post(String path, {dynamic data});
  // Future<Response> put(String path, {dynamic data});
  // Future<Response> delete(String path);
}
```

#### 2.2 API 엔드포인트 매핑 (GET 전용)
```dart
class Endpoints {
  // Customer
  static String customerList = '/api/customers';
  static String customerDetail(int id) => '/api/customers/$id';
  static String customerCreate = '/api/customers/create';  // GET 방식
  static String customerUpdate(int id) => '/api/customers/$id/update';  // GET 방식
  static String customerDelete(int id) => '/api/customers/$id/delete';  // GET 방식
  static String customerByEmail(String email) => '/api/customers?email=$email';
  static String customerByPhone(String phone) => '/api/customers?phone=$phone';
  
  // Product
  static String productList = '/api/products';
  static String productDetail(int id) => '/api/products/$id';
  static String productCreate = '/api/products/create';  // GET 방식
  static String productUpdate(int id) => '/api/products/$id/update';  // GET 방식
  static String productDelete(int id) => '/api/products/$id/delete';  // GET 방식
  static String productByProductBase(int pbid) => '/api/products?pbid=$pbid';
  static String productByManufacturer(int mfid) => '/api/products?mfid=$mfid';
  // ...
}
```

#### 2.3 테이블별 API 서비스 (GET 전용)
```dart
class CustomerApiService {
  final ApiClient _apiClient;
  
  Future<List<Customer>> getAll() async {
    final response = await _apiClient.get(Endpoints.customerList);
    return (response.data as List)
        .map((e) => Customer.fromMap(e))
        .toList();
  }
  
  Future<Customer?> getById(int id) async {
    final response = await _apiClient.get(Endpoints.customerDetail(id));
    return Customer.fromMap(response.data);
  }
  
  // GET 방식으로 생성 (임시)
  Future<int> create(Customer customer) async {
    final queryParams = customer.toMap();
    final response = await _apiClient.get(
      Endpoints.customerCreate,
      queryParams: queryParams,
    );
    return response.data['id'] as int;
  }
  
  // GET 방식으로 수정 (임시)
  Future<int> update(int id, Customer customer) async {
    final queryParams = customer.toMap();
    final response = await _apiClient.get(
      Endpoints.customerUpdate(id),
      queryParams: queryParams,
    );
    return response.data['affectedRows'] as int;
  }
  
  // GET 방식으로 삭제 (임시)
  Future<int> delete(int id) async {
    final response = await _apiClient.get(Endpoints.customerDelete(id));
    return response.data['affectedRows'] as int;
  }
}
```

### Phase 3: Handler 마이그레이션

#### 3.1 Handler 변경 전략
```dart
// 기존
class CustomerHandler {
  final DatabaseManager _dbManager = DatabaseManager();
  
  Future<Database> _getDatabase() async {
    return await _dbManager.getDatabase();
  }
  
  Future<List<Customer>> queryAll() async {
    final db = await _getDatabase();
    final results = await db.query(config.kTableCustomer);
    return results.map((e) => Customer.fromMap(e)).toList();
  }
}

// 변경 후
class CustomerHandler {
  final DatabaseAdapter _adapter;
  
  CustomerHandler({DatabaseAdapter? adapter}) 
    : _adapter = adapter ?? SQLiteAdapter(); // 기본값은 SQLite
  
  Future<List<Customer>> queryAll() async {
    final results = await _adapter.query(config.kTableCustomer);
    return results.map((e) => Customer.fromMap(e)).toList();
  }
}
```

#### 3.2 Config로 Adapter 선택
```dart
// config.dart
const bool kUseLocalDB = true; // false로 변경 시 API 사용

DatabaseAdapter createDatabaseAdapter() {
  if (kUseLocalDB) {
    return SQLiteAdapter();
  } else {
    return APIAdapter(
      baseUrl: 'https://api.example.com',
    );
  }
}
```

### Phase 4: 복합 쿼리 처리

#### 4.1 조인 쿼리 → API 엔드포인트 (GET 전용)
```dart
// 기존: rawQuery로 조인
final results = await db.rawQuery('''
  SELECT Purchase.*, Customer.cName
  FROM Purchase
  JOIN Customer ON Purchase.cid = Customer.id
  WHERE Purchase.id = ?
''', [purchaseId]);

// 변경: API 엔드포인트 (GET 방식)
final response = await _apiClient.get(
  '/api/purchases/$purchaseId/with-customer'
);
// 모든 조인 쿼리도 GET 방식으로 처리
```

#### 4.2 PurchaseService 변경
```dart
class PurchaseService {
  final PurchaseHandler _purchaseHandler;
  final PurchaseItemHandler _purchaseItemHandler;
  
  PurchaseService({
    PurchaseHandler? purchaseHandler,
    PurchaseItemHandler? purchaseItemHandler,
  }) : _purchaseHandler = purchaseHandler ?? PurchaseHandler(),
       _purchaseItemHandler = purchaseItemHandler ?? PurchaseItemHandler();
  
  // 기존 로직 유지, Handler만 교체
  Future<Map<String, dynamic>> queryOrderListWithItems(int purchaseId) async {
    // 기존 로직 그대로
  }
}
```

---

## API 스펙 설계

### RESTful API 설계 원칙

#### 기본 패턴 (1단계: GET만 사용)
```
GET    /api/{resource}           # 목록 조회
GET    /api/{resource}/{id}      # 상세 조회
GET    /api/{resource}/create?{params}    # 생성 (임시)
GET    /api/{resource}/{id}/update?{params}  # 수정 (임시)
GET    /api/{resource}/{id}/delete         # 삭제 (임시)
```

**⚠️ 중요**: 초기 구현은 **모든 통신을 GET 방식**으로 진행합니다.
- POST, PUT, DELETE는 차후 기능 완료 후 전환 검토 예정
- GET 방식으로 CRUD 모두 처리 (쿼리 파라미터 사용)
- 보안 및 RESTful 원칙은 2단계에서 개선

#### 엔드포인트 예시 (GET 전용)

**Customer**
```
GET    /api/customers                                    # 목록 조회
GET    /api/customers/{id}                              # 상세 조회
GET    /api/customers?email={email}                     # 이메일로 조회
GET    /api/customers?phone={phone}                     # 전화번호로 조회
GET    /api/customers/create?name={name}&email={email}&...  # 생성 (임시)
GET    /api/customers/{id}/update?name={name}&...       # 수정 (임시)
GET    /api/customers/{id}/delete                       # 삭제 (임시)
```

**Product**
```
GET    /api/products                                    # 목록 조회
GET    /api/products/{id}                               # 상세 조회
GET    /api/products?pbid={pbid}                        # ProductBase별 조회
GET    /api/products?mfid={mfid}                        # 제조사별 조회
GET    /api/products/create?pbid={pbid}&size={size}&... # 생성 (임시)
GET    /api/products/{id}/update?basePrice={price}&...  # 수정 (임시)
GET    /api/products/{id}/delete                       # 삭제 (임시)
```

**Purchase (복합 쿼리)**
```
GET    /api/purchases                                   # 목록 조회
GET    /api/purchases/{id}                             # 상세 조회
GET    /api/purchases/{id}/with-customer               # 고객 정보 포함
GET    /api/purchases/{id}/with-items                  # 주문 항목 포함
GET    /api/purchases/customer/{customerId}            # 고객별 주문 목록
GET    /api/purchases/returnable?customerId={id}      # 반품 가능 주문
GET    /api/purchases/create?cid={cid}&orderCode={code}&... # 생성 (임시)
GET    /api/purchases/{id}/update?pickupDate={date}&...     # 수정 (임시)
GET    /api/purchases/{id}/delete                      # 삭제 (임시)
```

**참고**: 
- 모든 생성/수정/삭제 작업은 현재 GET 방식으로 처리
- 쿼리 파라미터로 데이터 전달
- 차후 POST/PUT/DELETE로 전환 예정

### 요청/응답 형식 (GET 전용)

#### 요청 예시 (GET 방식)
```
GET /api/customers/create?cName=홍길동&cEmail=hong@example.com&cPhoneNumber=010-1234-5678&cPassword=hashed_password
```

**주의사항**:
- URL 인코딩 필요 (한글, 특수문자)
- 긴 데이터는 URL 길이 제한 고려
- 보안상 민감한 정보(비밀번호)는 GET 방식 부적절하나, 1단계에서는 허용

#### 응답 예시
```json
{
  "id": 1,
  "cName": "홍길동",
  "cEmail": "hong@example.com",
  "cPhoneNumber": "010-1234-5678",
  "cPassword": "hashed_password"
}
```

#### 에러 응답
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Customer not found",
    "details": {}
  }
}
```

---

## 데이터 마이그레이션

### SQLite → MySQL 마이그레이션

#### 1. 스키마 변환
- SQLite `INTEGER PRIMARY KEY AUTOINCREMENT` → MySQL `INT AUTO_INCREMENT PRIMARY KEY`
- SQLite `TEXT` → MySQL `VARCHAR` 또는 `TEXT`
- SQLite `REAL` → MySQL `DOUBLE` 또는 `DECIMAL`
- 인덱스 동일하게 생성

#### 2. 데이터 마이그레이션 스크립트
```python
# Python 스크립트 예시
import sqlite3
import mysql.connector
import json

# SQLite에서 데이터 추출
sqlite_conn = sqlite3.connect('bookstore.db')
sqlite_cursor = sqlite_conn.cursor()

# MySQL 연결
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='user',
    password='password',
    database='shoes_store'
)
mysql_cursor = mysql_conn.cursor()

# 테이블별 마이그레이션
tables = ['Customer', 'Employee', 'Product', 'Purchase', ...]

for table in tables:
    sqlite_cursor.execute(f'SELECT * FROM {table}')
    rows = sqlite_cursor.fetchall()
    
    for row in rows:
        # MySQL에 삽입
        # ...
```

#### 3. FastAPI 마이그레이션 엔드포인트
```python
# FastAPI에서 일괄 마이그레이션 지원
@app.post("/api/migrate/bulk")
async def bulk_migrate(data: List[Dict]):
    # 대량 데이터 삽입
    pass
```

---

## 테스트 전략

### 1. 단위 테스트
- Handler 테스트: SQLiteAdapter와 APIAdapter 모두 테스트
- API Client 테스트: Mock 서버 사용
- 모델 변환 테스트: JSON ↔ Dart 모델

### 2. 통합 테스트
- Handler → Adapter → API 전체 플로우
- 실제 FastAPI 서버와 연동 테스트

### 3. 성능 테스트
- SQLite vs API 응답 시간 비교
- 대량 데이터 처리 성능

### 4. 호환성 테스트
- 기존 기능 동작 확인
- Service 레이어 변경 없이 동작 확인

---

## 롤백 계획

### 1. Feature Flag
```dart
// config.dart
const bool kUseLocalDB = true; // false로 변경 시 API 사용
const bool kEnableAPIMode = false; // 점진적 활성화
```

### 2. 병행 운영
- SQLite와 API 모두 지원
- Config로 전환 가능
- 문제 발생 시 즉시 롤백

### 3. 데이터 동기화
- 마이그레이션 기간 동안 SQLite와 MySQL 동기화
- 양방향 동기화 또는 단방향 (SQLite → MySQL)

---

## 구현 우선순위

### Phase 1 (1-2주)
1. ✅ DatabaseAdapter 인터페이스 정의
2. ✅ SQLiteAdapter 구현
3. ✅ Handler에 Adapter 적용 (기본값 SQLite)
4. ✅ 테스트 및 검증

### Phase 2 (2-3주)
1. ✅ ApiClient 기본 구조 (GET 방식만)
2. ✅ Customer, Product 핵심 API 구현 (GET 전용)
3. ✅ APIAdapter 기본 구현 (GET 방식)
4. ✅ Handler에 APIAdapter 적용 테스트
5. ⚠️ GET 방식 제약사항 문서화 및 우회 방법 검토

### Phase 3 (2-3주)
1. ✅ 모든 Handler API 마이그레이션 (GET 방식)
2. ✅ 복합 쿼리 API 엔드포인트 구현 (GET 전용)
3. ✅ PurchaseService 마이그레이션
4. ✅ 통합 테스트
5. ⚠️ GET 방식의 한계점 문서화

### Phase 3.5 (차후 검토)
1. ⏳ POST/PUT/DELETE 방식 전환 계획 수립
2. ⏳ 보안 강화 (인증/인가)
3. ⏳ RESTful 원칙 준수
4. ⏳ API 버전 관리

### Phase 4 (1-2주)
1. ✅ 데이터 마이그레이션 스크립트
2. ✅ SQLite → MySQL 스키마 변환
3. ✅ 데이터 이관
4. ✅ 최종 검증 및 배포

---

## 주의사항

### 1. GET 방식 사용의 제약사항
- **URL 길이 제한**: 브라우저/서버별로 제한 있음 (일반적으로 2048자)
- **보안**: 민감한 정보(비밀번호 등)가 URL에 노출됨
- **캐싱**: GET 요청은 브라우저/프록시에서 캐싱될 수 있음
- **해결책**: 
  - 긴 데이터는 URL 인코딩 필수
  - 민감한 정보는 2단계에서 POST로 전환
  - 캐시 방지 헤더 추가 고려

### 2. 트랜잭션 처리
- SQLite: `db.transaction()` 사용
- API: FastAPI에서 트랜잭션 처리 필요
- 복합 작업은 API에서 원자성 보장
- GET 방식에서는 쿼리 파라미터로 트랜잭션 ID 전달 고려

### 3. 오프라인 지원
- 현재는 로컬 DB만 지원
- API 전환 시 오프라인 모드 고려 필요
- 캐싱 전략 검토

### 4. 에러 처리
- 네트워크 에러 처리
- 타임아웃 처리
- 재시도 로직

### 5. 보안 (1단계 제한사항)
- GET 방식은 보안에 취약
- URL에 민감한 정보 노출 가능
- 2단계에서 POST/PUT/DELETE 전환 시 보안 강화
- 현재는 개발/테스트 환경에서만 사용 권장

---

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Dio HTTP 클라이언트](https://pub.dev/packages/dio)
- [MySQL 마이그레이션 가이드](https://dev.mysql.com/doc/refman/8.0/en/migration.html)

---

**문서 버전**: 1.0  
**최종 수정일**: 2025-12-17  
**작성자**: AI Assistant

