# b_tnum (트랜잭션 번호) 주문 그룹화 기능 가이드

## 📋 개요

`b_tnum` (결제 트랜잭션 번호)는 **여러 `purchase_item`을 하나의 주문으로 묶는 용도**로 사용됩니다.

### 기존 구조 vs 새로운 구조

#### 기존 구조 (2단계)
```
Purchase (주문)
  ├─ id (PK)
  ├─ cid (FK → Customer)
  ├─ orderCode
  └─ timeStamp
      │
      └─ PurchaseItem (주문 항목들)
          ├─ id (PK)
          ├─ pcid (FK → Purchase.id)  ← 주문 그룹화
          ├─ pid (FK → Product)
          └─ ...
```

#### 새로운 구조 (단일 테이블 + b_tnum)
```
purchase_item (구매 내역)
  ├─ b_seq (PK)
  ├─ b_tnum (트랜잭션 번호)  ← 주문 그룹화 키
  ├─ u_seq (FK → user)
  ├─ p_seq (FK → product)
  └─ ...
```

---

## ✅ b_tnum 사용 방법

### 1. 주문 생성 시

**같은 주문의 모든 항목에 동일한 `b_tnum` 부여**

```sql
-- 주문 번호 생성
SET @order_number = 'TXN-20250101-001';

-- 첫 번째 항목
INSERT INTO purchase_item (br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum)
VALUES (1, 1, 1, 150000, 1, NOW(), @order_number);

-- 두 번째 항목 (같은 주문)
INSERT INTO purchase_item (br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum)
VALUES (1, 1, 2, 200000, 2, NOW(), @order_number);

-- 세 번째 항목 (같은 주문)
INSERT INTO purchase_item (br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum)
VALUES (1, 1, 3, 100000, 1, NOW(), @order_number);
```

**결과**: 3개의 `purchase_item`이 하나의 주문(`TXN-20250101-001`)으로 묶임

---

### 2. 주문 조회 시

#### 주문 목록 조회 (고객별)
```sql
-- 고객의 모든 주문 목록 (b_tnum으로 그룹화)
SELECT 
    b_tnum AS order_number,
    COUNT(*) AS item_count,
    SUM(b_quantity) AS total_quantity,
    SUM(b_price * b_quantity) AS total_amount,
    MIN(b_date) AS order_date
FROM purchase_item
WHERE u_seq = 1
GROUP BY b_tnum
ORDER BY order_date DESC;
```

**결과 예시**:
```
order_number      | item_count | total_quantity | total_amount | order_date
------------------|------------|----------------|--------------|------------------
TXN-20250101-001  | 3          | 4              | 650000       | 2025-01-01 10:00
TXN-20250101-002  | 2          | 3              | 450000       | 2025-01-01 11:00
```

#### 주문 상세 조회 (특정 주문의 모든 항목)
```sql
-- 특정 주문의 모든 항목 조회
SELECT 
    b_seq,
    p_seq,
    b_quantity,
    b_price,
    (b_price * b_quantity) AS item_total
FROM purchase_item
WHERE b_tnum = 'TXN-20250101-001'
ORDER BY b_seq;
```

**결과 예시**:
```
b_seq | p_seq | b_quantity | b_price | item_total
------|-------|------------|---------|------------
1     | 1     | 1          | 150000  | 150000
2     | 2     | 2          | 200000  | 400000
3     | 3     | 1          | 100000  | 100000
```

---

### 3. 주문 통계 조회

#### 일별 주문 통계
```sql
SELECT 
    DATE(b_date) AS order_date,
    COUNT(DISTINCT b_tnum) AS order_count,
    COUNT(*) AS item_count,
    SUM(b_price * b_quantity) AS total_revenue
FROM purchase_item
WHERE b_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(b_date)
ORDER BY order_date DESC;
```

#### 지점별 주문 통계
```sql
SELECT 
    br_seq,
    COUNT(DISTINCT b_tnum) AS order_count,
    COUNT(*) AS item_count,
    SUM(b_price * b_quantity) AS total_revenue
FROM purchase_item
GROUP BY br_seq;
```

---

## 🔍 인덱스 활용

### b_tnum 인덱스의 중요성

```sql
-- 인덱스가 있으면 빠른 조회
CREATE INDEX idx_purchase_item_b_tnum ON purchase_item(b_tnum);
```

**인덱스 사용 확인**:
```sql
EXPLAIN SELECT * FROM purchase_item WHERE b_tnum = 'TXN-20250101-001';
```

**결과**: `idx_purchase_item_b_tnum` 인덱스 사용 → 빠른 조회

---

## 💡 사용 시나리오

### 시나리오 1: 장바구니에서 주문 생성

```python
# Python 예시
order_number = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

cart_items = [
    {'p_seq': 1, 'quantity': 2, 'price': 150000},
    {'p_seq': 2, 'quantity': 1, 'price': 200000},
    {'p_seq': 3, 'quantity': 3, 'price': 100000},
]

for item in cart_items:
    cursor.execute("""
        INSERT INTO purchase_item 
        (br_seq, u_seq, p_seq, b_price, b_quantity, b_date, b_tnum)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (branch_id, user_id, item['p_seq'], item['price'], 
          item['quantity'], datetime.now(), order_number))
```

**결과**: 3개 항목이 하나의 주문(`order_number`)으로 묶임

---

### 시나리오 2: 주문 내역 조회

```python
# 주문 목록 조회
cursor.execute("""
    SELECT 
        b_tnum,
        COUNT(*) AS item_count,
        SUM(b_price * b_quantity) AS total_amount,
        MIN(b_date) AS order_date
    FROM purchase_item
    WHERE u_seq = %s
    GROUP BY b_tnum
    ORDER BY order_date DESC
""", (user_id,))

orders = cursor.fetchall()
# 결과: [(order_number, item_count, total_amount, order_date), ...]
```

---

## ⚠️ 주의사항

### 1. NULL 값 처리

`b_tnum`은 NULL일 수 있으므로, NULL 체크 필요:

```sql
-- NULL이 아닌 주문만 조회
SELECT * FROM purchase_item 
WHERE b_tnum IS NOT NULL 
  AND b_tnum = 'TXN-20250101-001';
```

### 2. 주문 번호 생성 규칙

권장 형식:
- `TXN-YYYYMMDD-HHMMSS-XXXX` (날짜 + 시간 + 랜덤)
- `TXN-YYYYMMDD-XXXXXX` (날짜 + 순차번호)
- UUID 사용도 가능

### 3. 트랜잭션 처리

여러 항목을 하나의 주문으로 묶을 때는 **트랜잭션 사용 권장**:

```python
try:
    conn.begin()
    order_number = generate_order_number()
    
    for item in cart_items:
        insert_purchase_item(item, order_number)
    
    conn.commit()
except:
    conn.rollback()
```

---

## 📊 기존 구조와의 비교

| 기능 | 기존 구조 | 새로운 구조 (b_tnum) |
|------|----------|---------------------|
| 주문 그룹화 | `Purchase.id` → `PurchaseItem.pcid` | `b_tnum` (같은 값) |
| 주문 조회 | JOIN 필요 | WHERE b_tnum = ? |
| 주문 목록 | Purchase 테이블 조회 | GROUP BY b_tnum |
| 데이터 구조 | 2개 테이블 | 1개 테이블 |
| 유연성 | 낮음 (Purchase 필수) | 높음 (b_tnum 선택적) |

---

## ✅ 결론

**`b_tnum`은 여러 `purchase_item`을 하나의 주문으로 묶는 용도로 정상적으로 사용 가능합니다!**

### 장점:
1. ✅ 단일 테이블 구조로 간단함
2. ✅ GROUP BY로 쉽게 주문 단위 집계 가능
3. ✅ 인덱스로 빠른 조회 가능
4. ✅ NULL 허용으로 유연한 사용 가능

### 사용 방법:
- 주문 생성: 모든 항목에 동일한 `b_tnum` 부여
- 주문 조회: `WHERE b_tnum = '주문번호'`
- 주문 목록: `GROUP BY b_tnum`

