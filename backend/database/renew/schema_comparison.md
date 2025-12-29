# 스키마 비교 분석 리포트

**작성일**: 2025-01-XX  
**비교 대상**:
- 기존: `backend/database/schema.sql`
- 새로운: `shoes_shop_db_mysql_init.sql`

---

## 🔍 주요 차이점 및 문제점

### 1. FOREIGN KEY 제약조건 - CASCADE 옵션 누락 ⚠️

#### 기존 스키마 (권장)
```sql
FOREIGN KEY (pbid) REFERENCES ProductBase(id) ON DELETE CASCADE
FOREIGN KEY (cid) REFERENCES Customer(id) ON DELETE CASCADE
```

#### 새로운 스키마 (문제)
```sql
CONSTRAINT fk_staff_branch FOREIGN KEY (br_seq) REFERENCES branch(br_seq)
-- CASCADE 옵션 없음!
```

**문제점**:
- 부모 레코드 삭제 시 자식 레코드 처리 방식이 명시되지 않음
- 기본값은 `RESTRICT`로, 부모 삭제 시 자식이 있으면 에러 발생
- 데이터 무결성은 보장되지만, 운영 중 삭제 시 문제 발생 가능

**권장 수정**:
```sql
CONSTRAINT fk_staff_branch 
  FOREIGN KEY (br_seq) REFERENCES branch(br_seq) 
  ON DELETE RESTRICT  -- 또는 ON DELETE SET NULL (비즈니스 로직에 따라)
  ON UPDATE CASCADE
```

---

### 2. 인덱스 설정 부족 ⚠️⚠️

#### 기존 스키마
```sql
UNIQUE INDEX idx_customer_email (cEmail),
UNIQUE INDEX idx_customer_phone (cPhoneNumber),
INDEX idx_purchase_cid (cid),
INDEX idx_purchase_item_pcid (pcid),
INDEX idx_purchase_item_pid (pid),
INDEX idx_purchase_item_status (pcStatus)
```

#### 새로운 스키마
- **인덱스가 거의 없음!**
- FOREIGN KEY는 자동으로 인덱스를 생성하지만, 조회 성능을 위한 인덱스 부족

**문제점**:
- `user.u_id` (로그인 ID) - UNIQUE 인덱스 없음 → 중복 가능성
- `user.u_phone` - UNIQUE 인덱스 없음 → 중복 가능성
- `purchase_item.b_tnum` (트랜잭션 번호) - 인덱스 없음 → 조회 성능 저하
- `purchase_item.b_date` - 인덱스 없음 → 날짜별 조회 성능 저하
- `product.p_name` - 인덱스 없음 → 검색 성능 저하

**권장 추가 인덱스**:
```sql
-- user 테이블
UNIQUE INDEX idx_user_id (u_id),
UNIQUE INDEX idx_user_phone (u_phone),

-- purchase_item 테이블
INDEX idx_purchase_item_b_tnum (b_tnum),  -- 트랜잭션 번호 조회
INDEX idx_purchase_item_b_date (b_date),  -- 날짜별 조회
INDEX idx_purchase_item_u_seq (u_seq),    -- 고객별 조회
INDEX idx_purchase_item_br_seq (br_seq),  -- 지점별 조회

-- product 테이블
INDEX idx_product_p_name (p_name),        -- 제품명 검색
INDEX idx_product_m_seq (m_seq),         -- 제조사별 조회

-- staff 테이블
INDEX idx_staff_br_seq (br_seq),         -- 지점별 직원 조회
```

---

### 3. NOT NULL 제약조건 누락 ⚠️

#### 기존 스키마
```sql
cEmail VARCHAR(255) NOT NULL,
cPhoneNumber VARCHAR(50) NOT NULL,
cName VARCHAR(255) NOT NULL,
cPassword VARCHAR(255) NOT NULL,
```

#### 새로운 스키마
```sql
u_id       VARCHAR(50)  COMMENT '고객 로그인 ID',  -- NOT NULL 없음!
u_password VARCHAR(255) COMMENT '고객 비밀번호(해시)',  -- NOT NULL 없음!
u_name     VARCHAR(50)  COMMENT '고객 이름',  -- NOT NULL 없음!
```

**문제점**:
- 필수 필드에 NOT NULL 제약이 없으면 NULL 값 삽입 가능
- 애플리케이션 레벨에서만 검증해야 함 → 데이터 무결성 약화

**권장 수정**:
```sql
u_id       VARCHAR(50)  NOT NULL COMMENT '고객 로그인 ID',
u_password VARCHAR(255) NOT NULL COMMENT '고객 비밀번호(해시)',
u_name     VARCHAR(50)  NOT NULL COMMENT '고객 이름',
u_phone    VARCHAR(30)  NOT NULL COMMENT '고객 전화번호',
```

---

### 4. UNIQUE 제약조건 누락 ⚠️

#### 기존 스키마
```sql
UNIQUE INDEX idx_customer_email (cEmail),
UNIQUE INDEX idx_customer_phone (cPhoneNumber),
UNIQUE INDEX idx_purchase_order_code (orderCode),
UNIQUE INDEX idx_product_pbid_size (pbid, size)
```

#### 새로운 스키마
- `user.u_id` - UNIQUE 없음
- `user.u_phone` - UNIQUE 없음
- `maker.m_name` - UNIQUE 없음
- `product` - UNIQUE 제약이 있지만 논리적으로 부족할 수 있음

**문제점**:
- 동일한 로그인 ID로 여러 계정 생성 가능
- 동일한 전화번호로 여러 계정 생성 가능
- 동일한 제조사명 중복 가능

**권장 수정**:
```sql
-- user 테이블
UNIQUE INDEX idx_user_id (u_id),
UNIQUE INDEX idx_user_phone (u_phone),

-- maker 테이블
UNIQUE INDEX idx_maker_name (m_name),

-- 카테고리 테이블들
UNIQUE INDEX idx_kind_category_name (kc_name),
UNIQUE INDEX idx_color_category_name (cc_name),
UNIQUE INDEX idx_size_category_name (sc_name),
UNIQUE INDEX idx_gender_category_name (gc_name),
```

---

### 5. 데이터 타입 및 길이 제약 ⚠️

#### 비교

| 필드 | 기존 | 새로운 | 문제점 |
|------|------|--------|--------|
| 고객 이름 | `VARCHAR(255)` | `VARCHAR(50)` | 길이 제한이 너무 짧음 |
| 제품명 | `VARCHAR(255)` | `VARCHAR(200)` | 약간 짧음 |
| 제조사명 | `VARCHAR(255)` | `VARCHAR(100)` | 짧을 수 있음 |
| 직원 직급 | `VARCHAR(100)` | `VARCHAR(30)` | 매우 짧음 |

**권장 수정**:
```sql
u_name     VARCHAR(255) NOT NULL,  -- 50 → 255
p_name     VARCHAR(255),           -- 200 → 255
m_name     VARCHAR(255),           -- 100 → 255
s_rank     VARCHAR(100),          -- 30 → 100
```

---

### 6. 기본값(DEFAULT) 설정 누락 ⚠️

#### 기존 스키마
```sql
pQuantity INT NOT NULL DEFAULT 0,
```

#### 새로운 스키마
```sql
p_stock INT NOT NULL DEFAULT 0,  -- ✅ 있음
-- 하지만 다른 필드들에 DEFAULT 없음
```

**권장 추가**:
```sql
-- purchase_item
b_price    INT DEFAULT 0 COMMENT '구매 당시 가격',
b_quantity INT DEFAULT 1 COMMENT '구매 수량',

-- receive, request
rec_quantity INT DEFAULT 0,
req_quantity INT DEFAULT 0,
```

---

### 7. 문자셋(Charset) 설정 ⚠️

#### 기존 스키마
```sql
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

#### 새로운 스키마
```sql
ENGINE=InnoDB COMMENT='...';
-- 테이블 레벨 문자셋 설정 없음
```

**문제점**:
- 데이터베이스 레벨에서만 문자셋 설정
- 테이블별로 다른 문자셋 사용 시 문제 가능성

**권장 수정**:
```sql
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='...';
```

---

### 8. 날짜/시간 필드 타입 ⚠️

#### 기존 스키마
```sql
pickupDate VARCHAR(50),  -- 문자열로 저장
timeStamp VARCHAR(50),   -- 문자열로 저장
```

#### 새로운 스키마
```sql
b_date     DATETIME COMMENT '구매 일시',  -- ✅ DATETIME 사용
pic_date   DATETIME COMMENT '수령 완료 일시',  -- ✅ DATETIME 사용
ref_date   DATETIME COMMENT '반품 처리 일시',  -- ✅ DATETIME 사용
```

**개선점**: 새로운 스키마가 DATETIME을 사용하여 더 나음!

---

### 9. 제약조건 명명 규칙 ⚠️

#### 기존 스키마
- 인덱스: `idx_테이블명_컬럼명` 형식
- 명확하고 일관성 있음

#### 새로운 스키마
- FOREIGN KEY: `fk_테이블명_참조테이블명` 형식
- UNIQUE: `uq_테이블명_컬럼명` 형식
- 일관성은 있지만, 인덱스 명명 규칙 부족

---

## 📊 종합 평가

### 심각도별 문제점

#### 🔴 높음 (즉시 수정 권장)
1. **인덱스 부족** - 조회 성능 저하
2. **UNIQUE 제약조건 누락** - 데이터 중복 가능성
3. **NOT NULL 제약조건 누락** - 필수 필드 NULL 허용

#### 🟡 중간 (수정 권장)
4. **FOREIGN KEY CASCADE 옵션** - 삭제 동작 불명확
5. **데이터 타입 길이** - 일부 필드 길이 부족
6. **문자셋 명시** - 테이블 레벨 문자셋 설정

#### 🟢 낮음 (선택적 개선)
7. **기본값 설정** - 일부 필드에 DEFAULT 추가
8. **제약조건 명명 규칙** - 인덱스 명명 규칙 통일

---

## ✅ 개선된 스키마 권장사항

### 1. user 테이블 개선
```sql
CREATE TABLE user (
  u_seq      INT AUTO_INCREMENT PRIMARY KEY COMMENT '고객 고유 ID(PK)',
  u_id       VARCHAR(50)  NOT NULL COMMENT '고객 로그인 ID',
  u_password VARCHAR(255) NOT NULL COMMENT '고객 비밀번호(해시)',
  u_name     VARCHAR(255) NOT NULL COMMENT '고객 이름',
  u_phone    VARCHAR(30)  NOT NULL COMMENT '고객 전화번호',
  u_image    MEDIUMBLOB   NULL COMMENT '고객 프로필 이미지',
  
  UNIQUE INDEX idx_user_id (u_id),
  UNIQUE INDEX idx_user_phone (u_phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='고객 계정 정보';
```

### 2. purchase_item 테이블 개선
```sql
CREATE TABLE purchase_item (
  b_seq      INT AUTO_INCREMENT PRIMARY KEY COMMENT '구매 고유 ID(PK)',
  br_seq     INT NOT NULL COMMENT '수령 지점 ID(FK)',
  u_seq      INT NOT NULL COMMENT '구매 고객 ID(FK)',
  p_seq      INT NOT NULL COMMENT '구매 제품 ID(FK)',
  b_price    INT DEFAULT 0 COMMENT '구매 당시 가격',
  b_quantity INT DEFAULT 1 COMMENT '구매 수량',
  b_date     DATETIME NOT NULL COMMENT '구매 일시',
  b_tnum     VARCHAR(100) COMMENT '결제 트랜잭션 번호',
  
  CONSTRAINT fk_purchase_branch  
    FOREIGN KEY (br_seq) REFERENCES branch(br_seq) 
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_purchase_user    
    FOREIGN KEY (u_seq) REFERENCES user(u_seq) 
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_purchase_product 
    FOREIGN KEY (p_seq) REFERENCES product(p_seq) 
    ON DELETE RESTRICT ON UPDATE CASCADE,
  
  INDEX idx_purchase_item_b_tnum (b_tnum),
  INDEX idx_purchase_item_b_date (b_date),
  INDEX idx_purchase_item_u_seq (u_seq),
  INDEX idx_purchase_item_br_seq (br_seq)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='고객 구매 내역';
```

---

## 🎯 결론

새로운 스키마는 **구조적으로는 잘 설계**되었지만, **데이터베이스 제약조건과 인덱스 설정이 부족**합니다.

### 즉시 수정 필요:
1. ✅ 인덱스 추가 (특히 UNIQUE 인덱스)
2. ✅ NOT NULL 제약조건 추가
3. ✅ FOREIGN KEY CASCADE 옵션 명시

### 권장 수정:
4. ✅ 데이터 타입 길이 조정
5. ✅ 문자셋 명시
6. ✅ 기본값 설정

이러한 수정을 통해 **데이터 무결성**과 **조회 성능**을 크게 개선할 수 있습니다.

