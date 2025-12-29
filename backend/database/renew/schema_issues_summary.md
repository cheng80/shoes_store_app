# 스키마 문제점 요약

## 🔴 즉시 수정 필요 (Critical)

### 1. user 테이블
- ❌ `u_id`, `u_password`, `u_name`, `u_phone`에 NOT NULL 없음
- ❌ `u_id`, `u_phone`에 UNIQUE 인덱스 없음 → 중복 계정 생성 가능
- ❌ `u_name` 길이가 50 → 255로 확장 필요

### 2. purchase_item 테이블
- ❌ `b_tnum` (트랜잭션 번호) 인덱스 없음 → 조회 성능 저하
- ❌ `b_date` 인덱스 없음 → 날짜별 조회 성능 저하
- ❌ `b_date`에 NOT NULL 없음
- ❌ FOREIGN KEY에 CASCADE 옵션 없음

### 3. 카테고리 테이블들
- ❌ `kc_name`, `cc_name`, `sc_name`, `gc_name`에 UNIQUE 없음 → 중복 카테고리 생성 가능
- ❌ NOT NULL 제약조건 없음

### 4. maker 테이블
- ❌ `m_name`에 UNIQUE 없음 → 중복 제조사 생성 가능
- ❌ `m_name`에 NOT NULL 없음

---

## 🟡 수정 권장 (Important)

### 1. 인덱스 부족
- `product.p_name` - 제품명 검색용 인덱스 없음
- `staff.s_phone` - UNIQUE 인덱스 없음
- `branch.br_name` - UNIQUE 인덱스 없음

### 2. 데이터 타입 길이
- `staff.s_rank` - VARCHAR(30) → VARCHAR(100)
- `user.u_name` - VARCHAR(50) → VARCHAR(255)
- `maker.m_name` - VARCHAR(100) → VARCHAR(255)

### 3. 기본값 설정
- `purchase_item.b_price` - DEFAULT 0
- `purchase_item.b_quantity` - DEFAULT 1
- `receive.rec_quantity` - DEFAULT 0
- `request.req_quantity` - DEFAULT 0

---

## ✅ 개선 사항

### 1. 문자셋 설정
- ✅ 데이터베이스 레벨에서 utf8mb4 설정됨
- ⚠️ 테이블 레벨에서도 명시 권장

### 2. 날짜 타입
- ✅ DATETIME 사용 (기존 VARCHAR보다 우수)

### 3. FOREIGN KEY 인덱스
- ✅ FOREIGN KEY는 자동으로 인덱스 생성됨

---

## 📊 실제 테이블 검증 결과

### user 테이블
```
현재 상태:
- PRIMARY KEY만 존재
- 모든 필드가 DEFAULT NULL
- UNIQUE 인덱스 없음

문제:
- 동일한 u_id로 여러 계정 생성 가능
- 필수 필드에 NULL 삽입 가능
```

### purchase_item 테이블
```
현재 상태:
- FOREIGN KEY 인덱스만 존재 (자동 생성)
- b_tnum, b_date 인덱스 없음

문제:
- 트랜잭션 번호로 조회 시 풀 테이블 스캔
- 날짜별 조회 시 성능 저하
```

### product 테이블
```
현재 상태:
- UNIQUE 제약조건 있음 (uq_product_color_size_maker)
- FOREIGN KEY 인덱스 자동 생성됨
- p_name 인덱스 없음

문제:
- 제품명 검색 시 성능 저하
```

---

## 🎯 권장 조치사항

1. **즉시 실행**: `shoes_shop_db_mysql_init_improved.sql` 적용
2. **검증**: 인덱스 및 제약조건 확인
3. **테스트**: 더미 데이터 삽입 및 조회 성능 테스트

