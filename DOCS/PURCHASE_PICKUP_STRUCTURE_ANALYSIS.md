# Purchase Item과 Pickup 구조 분석

**질문**: `purchase_item` 생성 시 `pickup`도 함께 생성되어야 하는가?

---

## 📋 현재 구조

### 테이블 관계

```
purchase_item (구매 내역)
├─ b_seq (PK)
├─ br_seq (FK → branch) - 수령 지점
├─ u_seq (FK → user)
├─ p_seq (FK → product)
├─ b_date (구매 일시)
└─ b_tnum (트랜잭션 번호)

pickup (오프라인 수령)
├─ pic_seq (PK)
├─ b_seq (FK → purchase_item) - 1:1 관계
└─ pic_date (수령 완료 일시)
```

**관계**: `pickup.b_seq` → `purchase_item.b_seq` (1:1)

---

## 🤔 비즈니스 시나리오 분석

### 시나리오 1: 오프라인 매장 즉시 구매 및 즉시 수령

**흐름:**
1. 고객이 매장에서 제품 선택
2. 결제 완료 → `purchase_item` 생성 (`b_date` = 현재)
3. 즉시 제품 수령 → `pickup` 생성 (`pic_date` = 현재 또는 `b_date`와 동일)

**결론**: ✅ **함께 생성 가능** (거의 동시에 발생)

---

### 시나리오 2: 온라인 주문 후 매장 픽업

**흐름:**
1. 고객이 온라인으로 주문 → `purchase_item` 생성 (`b_date` = 주문 일시)
2. 매장에서 제품 준비 (1-2일 소요)
3. 고객이 매장 방문하여 수령 → `pickup` 생성 (`pic_date` = 수령 일시)

**결론**: ❌ **별도 생성 필요** (시간 차이 있음)

---

### 시나리오 3: 오프라인 매장 구매 후 나중에 수령

**흐름:**
1. 고객이 매장에서 제품 선택 및 결제 → `purchase_item` 생성 (`b_date` = 구매 일시)
2. 제품이 재고 부족으로 나중에 수령 예정
3. 제품 입고 후 고객이 매장 방문하여 수령 → `pickup` 생성 (`pic_date` = 수령 일시)

**결론**: ❌ **별도 생성 필요** (시간 차이 있음)

---

## 💡 구조 분석

### 옵션 1: 항상 함께 생성 (현재 수정된 코드)

**장점:**
- ✅ 구현 간단
- ✅ 즉시 수령 시나리오에 적합
- ✅ 데이터 일관성 보장 (모든 purchase_item에 pickup 존재)

**단점:**
- ❌ 나중에 수령하는 경우 `pic_date`를 나중에 업데이트해야 함
- ❌ 실제 수령 전에 pickup 레코드가 존재 (비즈니스 로직상 어색함)
- ❌ 수령하지 않은 경우 처리 어려움 (pickup 삭제? pic_date NULL?)

---

### 옵션 2: 별도 생성 (원래 구조)

**장점:**
- ✅ 실제 수령 시점에 pickup 생성 (비즈니스 로직상 자연스러움)
- ✅ 수령하지 않은 경우 pickup 레코드 없음 (명확함)
- ✅ 유연한 처리 가능

**단점:**
- ❌ purchase_item 생성 시 pickup도 생성해야 하는지 명확하지 않음
- ❌ API 호출 2번 필요 (또는 트랜잭션 처리 필요)

---

### 옵션 3: 하이브리드 (권장) ⭐

**구조:**
- `purchase_item` 생성 시 `pickup`도 함께 생성하되, `pic_date`는 **NULL**로 시작
- 실제 수령 시 `pickup.pic_date` 업데이트

**장점:**
- ✅ 모든 purchase_item에 pickup 존재 (데이터 일관성)
- ✅ `pic_date`가 NULL이면 "아직 수령 안 함", 값이 있으면 "수령 완료" (명확함)
- ✅ 비즈니스 로직상 자연스러움

**예시:**
```sql
-- 구매 시
INSERT INTO purchase_item (b_date, ...) VALUES ('2025-01-15 10:00:00', ...);
INSERT INTO pickup (b_seq, pic_date) VALUES (1, NULL);  -- 아직 수령 안 함

-- 수령 시
UPDATE pickup SET pic_date = '2025-01-20 14:00:00' WHERE b_seq = 1;
```

---

## 🎯 권장 구조

### 권장: 옵션 3 (하이브리드)

**이유:**
1. **데이터 일관성**: 모든 purchase_item에 pickup 존재
2. **비즈니스 로직 명확성**: `pic_date` NULL = 미수령, 값 있음 = 수령 완료
3. **유연성**: 즉시 수령이든 나중에 수령이든 모두 처리 가능

**구현:**
```python
# purchase_item 생성 시
def insert_purchase_item(...):
    # 1. purchase_item 생성
    b_seq = insert_purchase_item(...)
    
    # 2. pickup 생성 (pic_date = NULL)
    insert_pickup(b_seq=b_seq, pic_date=None)
    
    return {"b_seq": b_seq, "pic_seq": pic_seq}

# 실제 수령 시
def update_pickup_complete(b_seq: int):
    update_pickup(b_seq=b_seq, pic_date=datetime.now())
```

---

## 📊 비교표

| 항목 | 옵션 1 (함께 생성, pic_date=b_date) | 옵션 2 (별도 생성) | 옵션 3 (함께 생성, pic_date=NULL) ⭐ |
|------|-----------------------------------|-------------------|-----------------------------------|
| **구현 복잡도** | 낮음 | 중간 | 낮음 |
| **데이터 일관성** | 높음 | 낮음 | 높음 |
| **비즈니스 로직** | 어색함 (수령 전에 날짜 있음) | 자연스러움 | 자연스러움 |
| **유연성** | 낮음 | 높음 | 높음 |
| **즉시 수령** | ✅ 적합 | ⚠️ API 2번 호출 | ✅ 적합 |
| **나중 수령** | ⚠️ pic_date 업데이트 필요 | ✅ 적합 | ✅ 적합 |

---

## ✅ 최종 권장사항

**옵션 3 (하이브리드)** 권장:

1. **`purchase_item` 생성 시 `pickup`도 함께 생성**
   - `pic_date = NULL` (아직 수령 안 함)

2. **실제 수령 시 `pickup.pic_date` 업데이트**
   - `pic_date = 현재 시간` (수령 완료)

3. **조회 시**
   - `pic_date IS NULL` → "수령 대기 중"
   - `pic_date IS NOT NULL` → "수령 완료" (수령 일시 표시)

이렇게 하면:
- ✅ 모든 purchase_item에 pickup 존재 (데이터 일관성)
- ✅ 수령 상태가 명확함 (`pic_date` NULL 여부)
- ✅ 즉시 수령/나중 수령 모두 처리 가능

