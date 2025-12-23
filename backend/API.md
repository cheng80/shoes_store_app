# API 문서

FastAPI 백엔드 API 엔드포인트 문서입니다.

## 기본 규칙

- **기본 CRUD**: RESTful 방식 (GET, POST, PUT, DELETE)
- **필터링**: 쿼리 파라미터로 처리
- **복합 쿼리 (JOIN)**: 별도 엔드포인트로 제공
- **응답 형식**: `{"results": [...]}` 또는 `{"result": {...}}`
- **에러 응답**: `{"result": "Error", "message": "..."}`

---

## 1. Customer (고객)

### 기본 CRUD

#### GET /api/customers
모든 고객 조회 (필터링 가능)

**쿼리 파라미터:**
- `email` (optional): 이메일로 필터
- `phone` (optional): 전화번호로 필터
- `identifier` (optional): 이메일 또는 전화번호로 필터 (OR 조건)
- `order_by` (optional): 정렬 기준 (기본값: "id")
- `order` (optional): 정렬 방향 "asc" 또는 "desc" (기본값: "asc")

**예시:**
```bash
GET /api/customers
GET /api/customers?email=user@example.com
GET /api/customers?identifier=user@example.com
GET /api/customers?order_by=id&order=desc
```

#### GET /api/customers/{customer_id}
ID로 고객 조회

#### POST /api/customers
고객 생성

**요청 본문:**
```json
{
  "cEmail": "user@example.com",
  "cPhoneNumber": "010-1234-5678",
  "cName": "홍길동",
  "cPassword": "hashed_password"
}
```

#### PUT /api/customers/{customer_id}
고객 수정

#### DELETE /api/customers/{customer_id}
고객 삭제

---

## 2. Product (제품)

### 기본 CRUD

#### GET /api/products
모든 제품 조회 (필터링 및 정렬 가능)

**쿼리 파라미터:**
- `pbid` (optional): ProductBase ID로 필터
- `mfid` (optional): Manufacturer ID로 필터
- `size` (optional): 사이즈로 필터
- `order_by` (optional): 정렬 기준 "id", "size", "basePrice", "pQuantity" (기본값: "id")
- `order` (optional): 정렬 방향 "asc" 또는 "desc" (기본값: "asc")

**예시:**
```bash
GET /api/products
GET /api/products?pbid=1
GET /api/products?pbid=1&size=250
GET /api/products?order_by=size&order=asc
```

#### GET /api/products/{product_id}
ID로 제품 조회

#### POST /api/products
제품 생성

**요청 본문:**
```json
{
  "pbid": 1,
  "mfid": 1,
  "size": 250,
  "basePrice": 100000,
  "pQuantity": 30
}
```

#### PUT /api/products/{product_id}
제품 수정

#### DELETE /api/products/{product_id}
제품 삭제

### 복합 쿼리 (JOIN)

#### GET /api/products/{product_id}/with_base
제품 + ProductBase 정보 조인 조회

#### GET /api/products/{product_id}/with_base_and_manufacturer
제품 + ProductBase + Manufacturer 정보 조인 조회

#### GET /api/products/list/with_base?pbid=1
ProductBase별 제품 목록 + ProductBase 정보 조인 조회

---

## 3. Purchase (주문)

### 기본 CRUD

#### GET /api/purchases
모든 주문 조회 (필터링 및 정렬 가능)

**쿼리 파라미터:**
- `cid` (optional): Customer ID로 필터
- `order_code` (optional): 주문 코드로 필터
- `order_by` (optional): 정렬 기준 (기본값: "timeStamp")
- `order` (optional): 정렬 방향 "asc" 또는 "desc" (기본값: "desc")

**예시:**
```bash
GET /api/purchases
GET /api/purchases?cid=1
GET /api/purchases?order_code=ORDER-001
GET /api/purchases?cid=1&order_by=timeStamp&order=desc
```

#### GET /api/purchases/{purchase_id}
ID로 주문 조회

#### POST /api/purchases
주문 생성

**요청 본문:**
```json
{
  "cid": 1,
  "pickupDate": "2025-12-14",
  "orderCode": "ORDER-001",
  "timeStamp": "2025-12-13T10:00:00"
}
```

#### PUT /api/purchases/{purchase_id}
주문 수정

#### DELETE /api/purchases/{purchase_id}
주문 삭제

### 복합 쿼리 (JOIN)

#### GET /api/purchases/{purchase_id}/with_customer
주문 + 고객 정보 조인 조회

#### GET /api/purchases/list/with_customer?cid=1
고객별 주문 목록 + 고객 정보 조인 조회

---

## 4. PurchaseItem (주문 항목)

### 기본 CRUD

#### GET /api/purchase_items
모든 주문 항목 조회 (필터링 및 정렬 가능)

**쿼리 파라미터:**
- `pid` (optional): Product ID로 필터
- `pcid` (optional): Purchase ID로 필터
- `status` (optional): 상태로 필터
- `order_by` (optional): 정렬 기준 (기본값: "id")
- `order` (optional): 정렬 방향 "asc" 또는 "desc" (기본값: "asc")

**예시:**
```bash
GET /api/purchase_items
GET /api/purchase_items?pcid=1
GET /api/purchase_items?pid=1&status=제품 준비 중
```

#### GET /api/purchase_items/{purchase_item_id}
ID로 주문 항목 조회

#### POST /api/purchase_items
주문 항목 생성

**요청 본문:**
```json
{
  "pid": 1,
  "pcid": 1,
  "pcQuantity": 2,
  "pcStatus": "제품 준비 중"
}
```

#### PUT /api/purchase_items/{purchase_item_id}
주문 항목 수정

#### DELETE /api/purchase_items/{purchase_item_id}
주문 항목 삭제

### 복합 쿼리 (JOIN)

#### GET /api/purchase_items/{purchase_item_id}/with_product
주문 항목 + 제품 정보 조인 조회

#### GET /api/purchase_items/list/with_product?pcid=1
주문별 항목 + 제품 정보 조인 조회

#### GET /api/purchase_items/{purchase_item_id}/full_detail
주문 항목 전체 상세 정보 조회 (4개 테이블 JOIN)

#### GET /api/purchase_items/list/full_detail?pcid=1
주문별 항목 전체 상세 정보 조회 (서브쿼리 포함)

---

## 5. ProductBase (제품 기본 정보)

### 기본 CRUD

#### GET /api/product_bases
모든 ProductBase 조회 (필터링 및 정렬 가능)

**쿼리 파라미터:**
- `name` (optional): 이름으로 필터
- `color` (optional): 색상으로 필터
- `category` (optional): 카테고리로 필터
- `order_by` (optional): 정렬 기준 (기본값: "id")
- `order` (optional): 정렬 방향 "asc" 또는 "desc" (기본값: "asc")

#### GET /api/product_bases/{product_base_id}
ID로 ProductBase 조회

#### POST /api/product_bases
ProductBase 생성

#### PUT /api/product_bases/{product_base_id}
ProductBase 수정

#### DELETE /api/product_bases/{product_base_id}
ProductBase 삭제

### 복합 쿼리

#### GET /api/product_bases/{product_base_id}/with_images
ProductBase + 이미지 목록 조인 조회

#### GET /api/product_bases/list/with_first_image
ProductBase 목록 + 첫 번째 이미지 조인 조회

---

## 6. ProductImage (제품 이미지)

### 기본 CRUD

#### GET /api/product_images
모든 제품 이미지 조회

**쿼리 파라미터:**
- `pbid` (optional): ProductBase ID로 필터
- `order_by` (optional): 정렬 기준 (기본값: "id")
- `order` (optional): 정렬 방향 "asc" 또는 "desc" (기본값: "asc")

#### GET /api/product_images/{image_id}
ID로 제품 이미지 조회

#### POST /api/product_images
제품 이미지 생성

#### PUT /api/product_images/{image_id}
제품 이미지 수정

#### DELETE /api/product_images/{image_id}
제품 이미지 삭제

---

## 7. Manufacturer (제조사)

### 기본 CRUD

#### GET /api/manufacturers
모든 제조사 조회

#### GET /api/manufacturers/{manufacturer_id}
ID로 제조사 조회

#### POST /api/manufacturers
제조사 생성

**요청 본문:**
```json
{
  "mName": "Nike"
}
```

#### PUT /api/manufacturers/{manufacturer_id}
제조사 수정

#### DELETE /api/manufacturers/{manufacturer_id}
제조사 삭제

---

## 8. Employee (직원)

### 기본 CRUD

#### GET /api/employees
모든 직원 조회

#### GET /api/employees/{employee_id}
ID로 직원 조회

#### POST /api/employees
직원 생성

#### PUT /api/employees/{employee_id}
직원 수정

#### DELETE /api/employees/{employee_id}
직원 삭제

---

## 9. LoginHistory (로그인 이력)

### 기본 CRUD

#### GET /api/login_histories
모든 로그인 이력 조회

**쿼리 파라미터:**
- `cid` (optional): Customer ID로 필터
- `order_by` (optional): 정렬 기준 (기본값: "id")
- `order` (optional): 정렬 방향 "asc" 또는 "desc" (기본값: "desc")

#### GET /api/login_histories/{login_history_id}
ID로 로그인 이력 조회

#### POST /api/login_histories
로그인 이력 생성

#### PUT /api/login_histories/{login_history_id}
로그인 이력 수정

#### DELETE /api/login_histories/{login_history_id}
로그인 이력 삭제

---

## Flutter 사용 예시

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiClient {
  static const String baseUrl = 'http://127.0.0.1:8000';
  
  // GET 요청
  static Future<Map<String, dynamic>> get(String endpoint, {Map<String, String>? queryParams}) async {
    final uri = Uri.parse('$baseUrl$endpoint').replace(queryParameters: queryParams);
    final response = await http.get(uri);
    return jsonDecode(response.body);
  }
  
  // POST 요청
  static Future<Map<String, dynamic>> post(String endpoint, Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );
    return jsonDecode(response.body);
  }
  
  // PUT 요청
  static Future<Map<String, dynamic>> put(String endpoint, Map<String, dynamic> data) async {
    final response = await http.put(
      Uri.parse('$baseUrl$endpoint'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(data),
    );
    return jsonDecode(response.body);
  }
  
  // DELETE 요청
  static Future<Map<String, dynamic>> delete(String endpoint) async {
    final response = await http.delete(Uri.parse('$baseUrl$endpoint'));
    return jsonDecode(response.body);
  }
}

// 사용 예시
final products = await ApiClient.get('/api/products', queryParams: {'pbid': '1', 'size': '250'});
final product = await ApiClient.get('/api/products/1/with_base');
final result = await ApiClient.post('/api/customers', {
  'cEmail': 'user@example.com',
  'cPhoneNumber': '010-1234-5678',
  'cName': '홍길동',
  'cPassword': 'hashed_password'
});
```

