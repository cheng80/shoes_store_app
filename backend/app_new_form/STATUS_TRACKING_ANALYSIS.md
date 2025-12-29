# 주문/수령/반품 상태 추적 분석

**검토일**: 2025-01-XX  
**목적**: 신규 구조에서 상태 추적 가능 여부 검토

---

## 📋 기존 구조 vs 신규 구조 비교

### 기존 구조 (app_basic_form)

#### 1. 주문 상태 추적

**PurchaseItem 테이블:**
```sql
CREATE TABLE PurchaseItem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pid INT NOT NULL,
    pcid INT NOT NULL,
    pcQuantity INT NOT NULL,
    pcStatus VARCHAR(100) NOT NULL,  -- ✅ 상태 필드 존재
    ...
    INDEX idx_purchase_item_status (pcStatus)  -- 상태별 조회 가능
);
```

**상태 값 예시:**
- `"제품 준비 중"` (0)
- `"제품 배송 중"` (1)
- `"제품 수령 완료"` (2)
- `"반품 신청"` (3)
- `"반품 처리 중"` (4)
- `"반품 완료"` (5)

**상태 관리:**
- `OrderStatusUtils` 클래스로 상태 관리
- 상태별 조회, 필터링 가능
- 상태 변경 이력 추적 가능

---

### 신규 구조 (app_new_form)

#### 1. 주문 상태 추적

**purchase_item 테이블:**
```sql
CREATE TABLE purchase_item (
  b_seq      INT AUTO_INCREMENT PRIMARY KEY,
  br_seq     INT NOT NULL,
  u_seq      INT NOT NULL,
  p_seq      INT NOT NULL,
  b_price    INT DEFAULT 0,
  b_quantity INT DEFAULT 1,
  b_date     DATETIME NOT NULL,
  b_tnum     VARCHAR(100),
  -- ❌ 상태 필드 없음
);
```

**문제점:**
- ❌ 주문 상태 추적 불가능
- ❌ "주문 완료", "준비 중", "수령 대기" 등 상태 구분 불가
- ❌ 상태별 조회/필터링 불가

---

#### 2. 수령 상태 추적

**pickup 테이블:**
```sql
CREATE TABLE pickup (
  pic_seq  INT AUTO_INCREMENT PRIMARY KEY,
  b_seq    INT NOT NULL,
  pic_date DATETIME COMMENT '수령 완료 일시',
  -- ❌ 상태 필드 없음
);
```

**현재 추적 방법:**
- `pic_date IS NULL` → 수령 대기 중
- `pic_date IS NOT NULL` → 수령 완료

**문제점:**
- ⚠️ 2단계 상태만 추적 가능 (대기/완료)
- ❌ "수령 준비 중", "수령 가능", "수령 지연" 등 세부 상태 추적 불가
- ❌ 수령 상태 변경 이력 추적 불가

---

#### 3. 반품 상태 추적

**refund 테이블:**
```sql
CREATE TABLE refund (
  ref_seq    INT AUTO_INCREMENT PRIMARY KEY,
  ref_date   DATETIME COMMENT '반품 처리 일시',
  ref_reason VARCHAR(255) COMMENT '반품 사유',
  u_seq      INT NOT NULL,
  s_seq      INT NOT NULL,
  pic_seq    INT NOT NULL,
  -- ❌ 상태 필드 없음
);
```

**현재 추적 방법:**
- `refund` 레코드 존재 여부로만 판단
- `ref_date IS NULL` → 반품 처리 중?
- `ref_date IS NOT NULL` → 반품 완료?

**문제점:**
- ❌ 반품 상태 추적 불가능
- ❌ "반품 신청", "반품 검수 중", "반품 승인", "반품 거부", "반품 완료" 등 상태 구분 불가
- ❌ 반품 상태 변경 이력 추적 불가

---

## ⚠️ 문제점 요약

### 1. 주문 상태 추적 불가능

**기존:**
```
PurchaseItem.pcStatus:
- "제품 준비 중"
- "제품 배송 중"
- "제품 수령 완료"
- "반품 신청"
- "반품 완료"
```

**신규:**
```
purchase_item: 상태 필드 없음
→ 주문이 어떤 단계인지 알 수 없음
```

**영향:**
- 고객이 주문 상태를 확인할 수 없음
- 관리자가 주문 상태별로 조회/관리할 수 없음
- 주문 상태 변경 이력을 추적할 수 없음

---

### 2. 수령 상태 추적 제한적

**기존:**
```
PurchaseItem.pcStatus로 수령 상태도 함께 관리
```

**신규:**
```
pickup.pic_date:
- NULL → 수령 대기 중
- 값 있음 → 수령 완료
```

**영향:**
- 2단계 상태만 추적 가능 (대기/완료)
- "수령 준비 중", "수령 가능", "수령 지연" 등 세부 상태 추적 불가
- 수령 상태 변경 이력 추적 불가

---

### 3. 반품 상태 추적 불가능

**기존:**
```
PurchaseItem.pcStatus:
- "반품 신청"
- "반품 처리 중"
- "반품 완료"
```

**신규:**
```
refund: 상태 필드 없음
→ 반품이 어떤 단계인지 알 수 없음
```

**영향:**
- 고객이 반품 상태를 확인할 수 없음
- 관리자가 반품 상태별로 조회/관리할 수 없음
- 반품 상태 변경 이력을 추적할 수 없음

---

## 💡 개선 방안 제안

### 옵션 1: 통합 상태 필드 (권장) ⭐⭐⭐

**핵심 아이디어**: 주문 → 수령 → 반품은 순차적으로 일어나므로 하나의 상태 필드로 관리

#### purchase_item에 통합 상태 필드 추가

```sql
ALTER TABLE purchase_item 
  ADD COLUMN b_status VARCHAR(50) DEFAULT '주문 완료' COMMENT '주문/수령/반품 통합 상태';

-- 상태 값 (순차적 흐름):
-- 1. '주문 완료' (기본값)
-- 2. '준비 중'
-- 3. '수령 대기'
-- 4. '수령 완료'
-- 5. '반품 신청' (수령 완료 후)
-- 6. '반품 처리 중'
-- 7. '반품 완료'
-- 8. '취소' (주문 완료 후 취소)
```

**상태 흐름도:**
```
주문 완료 → 준비 중 → 수령 대기 → 수령 완료
                                    ↓
                              반품 신청 → 반품 처리 중 → 반품 완료
```

**장점:**
- ✅ 하나의 필드로 전체 프로세스 관리 (단순함)
- ✅ 상태별 조회/필터링 가능
- ✅ 기존 구조와 유사 (PurchaseItem.pcStatus와 동일한 개념)
- ✅ pickup, refund 테이블에 별도 상태 필드 불필요
- ✅ 데이터 일관성 유지 (하나의 소스)

**단점:**
- ❌ 테이블 구조 변경 필요 (하지만 한 번만)

**구현 예시:**
```python
# 주문 생성 시
INSERT INTO purchase_item (..., b_status) VALUES (..., '주문 완료');

# 준비 완료 시
UPDATE purchase_item SET b_status = '수령 대기' WHERE b_seq = ?;

# 수령 완료 시
UPDATE purchase_item SET b_status = '수령 완료' WHERE b_seq = ?;
INSERT INTO pickup (b_seq, pic_date) VALUES (?, NOW());

# 반품 신청 시
UPDATE purchase_item SET b_status = '반품 신청' WHERE b_seq = ?;
INSERT INTO refund (..., ref_status) VALUES (..., '반품 신청');

# 반품 완료 시
UPDATE purchase_item SET b_status = '반품 완료' WHERE b_seq = ?;
UPDATE refund SET ref_date = NOW() WHERE ref_seq = ?;
```

---

### 옵션 2: 각 테이블에 상태 필드 추가 (비권장)

#### 2.1 purchase_item에 상태 필드 추가

```sql
ALTER TABLE purchase_item 
  ADD COLUMN b_status VARCHAR(50) DEFAULT '주문 완료' COMMENT '주문 상태';
```

#### 2.2 pickup에 상태 필드 추가

```sql
ALTER TABLE pickup 
  ADD COLUMN pic_status VARCHAR(50) DEFAULT '수령 대기' COMMENT '수령 상태';
```

#### 2.3 refund에 상태 필드 추가

```sql
ALTER TABLE refund 
  ADD COLUMN ref_status VARCHAR(50) DEFAULT '반품 신청' COMMENT '반품 상태';
```

**단점:**
- ❌ 상태가 여러 테이블에 분산되어 관리 복잡
- ❌ 데이터 일관성 문제 가능성
- ❌ 조회 시 JOIN 필요
- ❌ 불필요한 중복

---

### 옵션 2: 상태 이력 테이블 추가 (고급)

```sql
CREATE TABLE status_history (
  sh_seq INT AUTO_INCREMENT PRIMARY KEY,
  b_seq INT COMMENT '구매 ID (FK)',
  pic_seq INT COMMENT '수령 ID (FK)',
  ref_seq INT COMMENT '반품 ID (FK)',
  sh_status VARCHAR(50) NOT NULL COMMENT '상태',
  sh_previous_status VARCHAR(50) COMMENT '이전 상태',
  sh_date DATETIME NOT NULL COMMENT '상태 변경 일시',
  sh_reason VARCHAR(255) COMMENT '상태 변경 사유',
  s_seq INT COMMENT '처리 직원 ID (FK)',
  
  INDEX idx_status_history_b_seq (b_seq),
  INDEX idx_status_history_pic_seq (pic_seq),
  INDEX idx_status_history_ref_seq (ref_seq),
  INDEX idx_status_history_status (sh_status),
  INDEX idx_status_history_date (sh_date)
);
```

**장점:**
- ✅ 상태 변경 이력 완전 추적 가능
- ✅ 언제, 누가, 왜 상태를 변경했는지 기록 가능
- ✅ 감사(audit) 용이

**단점:**
- ❌ 복잡한 구조
- ❌ 조회 쿼리 복잡도 증가

---

### 옵션 3: 하이브리드 (권장) ⭐

**구조:**
1. 각 테이블에 현재 상태 필드 추가 (옵션 1)
2. 상태 변경 이력은 별도 테이블로 관리 (옵션 2, 선택적)

**예시:**
```sql
-- 현재 상태 (빠른 조회용)
ALTER TABLE purchase_item ADD COLUMN b_status VARCHAR(50);
ALTER TABLE pickup ADD COLUMN pic_status VARCHAR(50);
ALTER TABLE refund ADD COLUMN ref_status VARCHAR(50);

-- 상태 변경 이력 (선택적, 필요시)
CREATE TABLE status_history (...);
```

**장점:**
- ✅ 현재 상태 빠른 조회 가능
- ✅ 상태 변경 이력 추적 가능 (선택적)
- ✅ 유연한 확장성

---

## 📊 비교표

| 항목 | 기존 구조 | 신규 구조 (현재) | 개선 후 (통합 상태) |
|------|----------|----------------|-------------------|
| **주문 상태 추적** | ✅ 가능 (pcStatus) | ❌ 불가능 | ✅ 가능 (b_status) |
| **수령 상태 추적** | ✅ 가능 (pcStatus) | ⚠️ 제한적 (pic_date만) | ✅ 가능 (b_status) |
| **반품 상태 추적** | ✅ 가능 (pcStatus) | ❌ 불가능 | ✅ 가능 (b_status) |
| **상태별 조회** | ✅ 가능 | ❌ 불가능 | ✅ 가능 |
| **상태 변경 이력** | ⚠️ 제한적 | ❌ 불가능 | ✅ 가능 (옵션 2) |
| **구조 단순성** | ✅ 단순 (1개 필드) | ✅ 단순 (상태 없음) | ✅ 단순 (1개 필드) |
| **데이터 일관성** | ✅ 높음 | ⚠️ 중간 | ✅ 높음 (하나의 소스) |

---

## ✅ 권장사항

### 즉시 수정 필요 (권장: 옵션 1)

**`purchase_item`에 통합 상태 필드 `b_status` 추가**

```sql
ALTER TABLE purchase_item 
  ADD COLUMN b_status VARCHAR(50) DEFAULT '주문 완료' 
  COMMENT '주문/수령/반품 통합 상태';

-- 인덱스 추가 (상태별 조회 성능 향상)
CREATE INDEX idx_purchase_item_b_status ON purchase_item(b_status);
```

**상태 값 정의:**
```sql
-- 주문 단계
'주문 완료'    -- 구매 완료 (기본값)
'준비 중'      -- 제품 준비 중
'수령 대기'    -- 수령 가능 상태

-- 수령 단계
'수령 완료'    -- 고객이 수령 완료

-- 반품 단계 (수령 완료 후)
'반품 신청'    -- 고객이 반품 요청
'반품 처리 중' -- 반품 검수/처리 중
'반품 완료'    -- 반품 처리 완료

-- 기타
'취소'         -- 주문 취소
```

**이유:**
- ✅ 주문 → 수령 → 반품은 순차적으로 일어나므로 하나의 상태로 관리 가능
- ✅ 기존 구조(PurchaseItem.pcStatus)와 동일한 개념
- ✅ 단순하고 명확한 구조
- ✅ pickup, refund 테이블에 별도 상태 필드 불필요

### 선택적 개선

**`status_history` 테이블 추가** (선택적)
- 상태 변경 이력 추적
- 감사(audit) 목적
- 필요시 추가 고려

---

## 🎯 결론

**현재 신규 구조는 상태 추적 기능이 부족합니다.**

- ❌ 주문 상태 추적 불가능
- ⚠️ 수령 상태 추적 제한적 (2단계만)
- ❌ 반품 상태 추적 불가능

**권장 조치:**
- ✅ **`purchase_item`에 통합 상태 필드 `b_status` 추가** (옵션 1 권장)
- ✅ 주문 → 수령 → 반품은 순차적으로 일어나므로 하나의 상태 필드로 관리 가능
- ✅ 기존 구조(PurchaseItem.pcStatus)와 동일한 개념
- ✅ pickup, refund 테이블에는 별도 상태 필드 불필요
- ⚠️ 필요시 상태 변경 이력 테이블 추가 고려

**최종 권장 구조:**
```sql
-- purchase_item에만 상태 필드 추가
ALTER TABLE purchase_item 
  ADD COLUMN b_status VARCHAR(50) DEFAULT '주문 완료' 
  COMMENT '주문/수령/반품 통합 상태';

-- pickup, refund는 날짜 필드만으로 충분
-- (상태는 purchase_item.b_status로 관리)
```

