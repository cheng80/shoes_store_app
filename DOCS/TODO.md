# 신규 API 구조 개선 사항 (논의 필요)

**작성일**: 2025-01-XX  
**상태**: 🔄 논의 대기 중

---

## 📋 목차

1. [제품 이미지 다중 저장 기능](#1-제품-이미지-다중-저장-기능)
2. [로그인 히스토리 기능](#2-로그인-히스토리-기능)
3. [로그인 방식 변경 (이메일/전화번호)](#3-로그인-방식-변경-이메일전화번호)

---

## 1. 제품 이미지 다중 저장 기능

---

## 📋 현재 상태

### 현재 구조의 제한사항

**신규 ERD 구조 (`app_new_form`):**
- `product.p_image VARCHAR(255)` - 하나의 이미지 경로만 저장 가능
- 제품당 이미지 1장만 저장 가능

**기존 구조 (`app_basic_form`):**
- `ProductImage` 테이블 - 하나의 ProductBase에 여러 이미지 저장 가능
- 제품당 여러 이미지 저장 가능

---

## ⚠️ 문제점

1. **제품 상세 페이지 제한**
   - 여러 각도 이미지 표시 불가
   - 썸네일/상세 이미지 구분 불가
   - 이미지 갤러리 기능 구현 불가

2. **사용자 경험 저하**
   - 제품 상세 정보 제공에 제한
   - 이커머스 표준 기능 부재

---

## 💡 개선 방안 제안

### 옵션 1: 별도 테이블 추가 (권장) ⭐

```sql
CREATE TABLE product_image (
  pi_seq INT AUTO_INCREMENT PRIMARY KEY,
  p_seq INT NOT NULL COMMENT '제품 ID(FK)',
  pi_path VARCHAR(255) NOT NULL COMMENT '이미지 경로',
  pi_order INT DEFAULT 0 COMMENT '이미지 순서',
  pi_type VARCHAR(50) COMMENT '이미지 타입(thumbnail, detail 등)',
  
  CONSTRAINT fk_product_image_product
    FOREIGN KEY (p_seq) REFERENCES product(p_seq)
    ON DELETE CASCADE ON UPDATE CASCADE,
  
  INDEX idx_product_image_p_seq (p_seq)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**장점:**
- ✅ 정규화된 구조
- ✅ 이미지 순서 관리 가능
- ✅ 이미지 타입 구분 가능
- ✅ 확장성 우수

**단점:**
- ❌ 추가 테이블 관리 필요
- ❌ JOIN 쿼리 필요

---

### 옵션 2: JSON 배열로 저장

```sql
-- product 테이블 수정
ALTER TABLE product 
  MODIFY COLUMN p_image JSON COMMENT '이미지 경로 배열';
```

**예시 데이터:**
```json
["/images/product1_1.jpg", "/images/product1_2.jpg", "/images/product1_3.jpg"]
```

**장점:**
- ✅ 기존 테이블 구조 유지
- ✅ 간단한 구현

**단점:**
- ❌ 이미지 순서/타입 관리 어려움
- ❌ JSON 쿼리 복잡도 증가
- ❌ MySQL 5.7+ 필요

---

### 옵션 3: 콤마 구분 문자열

```sql
-- product 테이블 수정
ALTER TABLE product 
  MODIFY COLUMN p_image VARCHAR(1000) COMMENT '이미지 경로들 (콤마 구분)';
```

**예시 데이터:**
```
"/images/img1.jpg,/images/img2.jpg,/images/img3.jpg"
```

**장점:**
- ✅ 가장 간단한 구현
- ✅ 기존 구조 최소 변경

**단점:**
- ❌ 정규화 위반
- ❌ 이미지 순서/타입 관리 불가
- ❌ 문자열 파싱 필요

---

## 📝 논의 사항

### 결정 필요 사항

1. **비즈니스 요구사항**
   - 제품당 이미지 개수 제한이 있는가?
   - 이미지 순서 관리가 필요한가?
   - 썸네일/상세 이미지 구분이 필요한가?

2. **기술적 고려사항**
   - 성능 요구사항
   - 확장성 요구사항
   - 유지보수성

3. **마이그레이션 계획**
   - 기존 데이터 마이그레이션 방법
   - API 변경 범위
   - 클라이언트 코드 수정 범위

---

## 🔄 다음 단계

1. 개발팀과 논의 진행
2. 비즈니스 요구사항 확인
3. 개선 방안 결정
4. 스키마 수정 및 API 구현
5. 테스트 및 배포

---

## 📌 참고

- 현재 구조: `backend/database/renew/shoes_shop_db_mysql_init_improved.sql`
- 기존 구조 참고: `backend/app_basic_form/api/product_images.py`

---

## 2. 로그인 히스토리 기능

### 현재 상태의 제한사항

**신규 ERD 구조 (`app_new_form`):**
- `login_history` 테이블 없음
- 로그인 이력 추적 불가
- 보안 감사(audit) 불가

**기존 구조 (`app_basic_form`):**
- `LoginHistory` 테이블 존재
- 고객 로그인 이력 추적 가능
- 로그인 시간, 상태, 버전, 주소, 결제 방법 등 기록

---

### ⚠️ 문제점

1. **보안 감사 불가**
   - 로그인 시도 추적 불가
   - 비정상 로그인 감지 불가
   - 보안 이벤트 기록 없음

2. **사용자 활동 분석 불가**
   - 로그인 패턴 분석 불가
   - 사용자 행동 분석 불가
   - 마케팅 데이터 수집 불가

3. **컴플라이언스 이슈**
   - 개인정보보호법 준수 어려움
   - 보안 감사 대응 불가

---

### 💡 개선 방안 제안

#### 옵션 1: 통합 로그인 히스토리 테이블 (권장) ⭐

```sql
CREATE TABLE login_history (
  lh_seq INT AUTO_INCREMENT PRIMARY KEY COMMENT '로그인 히스토리 ID(PK)',
  u_seq INT COMMENT '고객 ID(FK, NULL 가능)',
  s_seq INT COMMENT '직원 ID(FK, NULL 가능)',
  lh_time DATETIME NOT NULL COMMENT '로그인 시각',
  lh_status VARCHAR(50) NOT NULL COMMENT '로그인 상태(success, failed 등)',
  lh_version VARCHAR(50) COMMENT '앱/웹 버전',
  lh_address VARCHAR(255) COMMENT '로그인 IP 주소',
  lh_device VARCHAR(255) COMMENT '디바이스 정보',
  lh_user_type ENUM('user', 'staff') NOT NULL COMMENT '사용자 타입',
  
  CONSTRAINT fk_login_history_user
    FOREIGN KEY (u_seq) REFERENCES user(u_seq)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_login_history_staff
    FOREIGN KEY (s_seq) REFERENCES staff(s_seq)
    ON DELETE SET NULL ON UPDATE CASCADE,
  
  INDEX idx_login_history_u_seq (u_seq),
  INDEX idx_login_history_s_seq (s_seq),
  INDEX idx_login_history_lh_time (lh_time),
  INDEX idx_login_history_lh_status (lh_status),
  INDEX idx_login_history_lh_user_type (lh_user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='로그인 히스토리';
```

**장점:**
- ✅ 고객과 직원 모두 추적 가능
- ✅ 통합 관리 용이
- ✅ 확장성 우수

**단점:**
- ❌ 하나의 테이블에 두 타입 혼재

---

#### 옵션 2: 분리된 로그인 히스토리 테이블

```sql
-- 고객 로그인 히스토리
CREATE TABLE user_login_history (
  ulh_seq INT AUTO_INCREMENT PRIMARY KEY,
  u_seq INT NOT NULL COMMENT '고객 ID(FK)',
  ulh_time DATETIME NOT NULL,
  ulh_status VARCHAR(50) NOT NULL,
  ulh_version VARCHAR(50),
  ulh_address VARCHAR(255),
  ulh_device VARCHAR(255),
  
  FOREIGN KEY (u_seq) REFERENCES user(u_seq)
    ON DELETE CASCADE ON UPDATE CASCADE,
  
  INDEX idx_user_login_history_u_seq (u_seq),
  INDEX idx_user_login_history_ulh_time (ulh_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 직원 로그인 히스토리
CREATE TABLE staff_login_history (
  slh_seq INT AUTO_INCREMENT PRIMARY KEY,
  s_seq INT NOT NULL COMMENT '직원 ID(FK)',
  slh_time DATETIME NOT NULL,
  slh_status VARCHAR(50) NOT NULL,
  slh_version VARCHAR(50),
  slh_address VARCHAR(255),
  slh_device VARCHAR(255),
  
  FOREIGN KEY (s_seq) REFERENCES staff(s_seq)
    ON DELETE CASCADE ON UPDATE CASCADE,
  
  INDEX idx_staff_login_history_s_seq (s_seq),
  INDEX idx_staff_login_history_slh_time (slh_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**장점:**
- ✅ 타입별 분리로 관리 용이
- ✅ 각 테이블 최적화 가능

**단점:**
- ❌ 테이블 중복
- ❌ 통합 조회 시 UNION 필요

---

#### 옵션 3: 기존 구조 유지 (고객만)

```sql
CREATE TABLE login_history (
  lh_seq INT AUTO_INCREMENT PRIMARY KEY,
  u_seq INT NOT NULL COMMENT '고객 ID(FK)',
  lh_time DATETIME NOT NULL COMMENT '로그인 시각',
  lh_status VARCHAR(50) NOT NULL COMMENT '로그인 상태',
  lh_version VARCHAR(50) COMMENT '앱 버전',
  lh_address VARCHAR(255) COMMENT 'IP 주소',
  lh_device VARCHAR(255) COMMENT '디바이스 정보',
  
  FOREIGN KEY (u_seq) REFERENCES user(u_seq)
    ON DELETE CASCADE ON UPDATE CASCADE,
  
  INDEX idx_login_history_u_seq (u_seq),
  INDEX idx_login_history_lh_time (lh_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**장점:**
- ✅ 기존 구조와 유사
- ✅ 간단한 구현

**단점:**
- ❌ 직원 로그인 추적 불가

---

### 📝 논의 사항

#### 결정 필요 사항

1. **비즈니스 요구사항**
   - 고객과 직원 모두 로그인 추적이 필요한가?
   - 로그인 실패 기록이 필요한가?
   - 로그인 히스토리 보관 기간은?

2. **보안 요구사항**
   - 보안 감사(audit) 요구사항
   - 컴플라이언스 요구사항
   - 이상 로그인 감지 필요 여부

3. **성능 고려사항**
   - 로그인 히스토리 데이터량 예상
   - 조회 빈도
   - 보관 정책 (아카이빙, 삭제)

---

### 🔄 다음 단계

1. 개발팀과 논의 진행
2. 보안/컴플라이언스 요구사항 확인
3. 개선 방안 결정
4. 스키마 수정 및 API 구현
5. 테스트 및 배포

---

### 📌 참고

- 기존 구조: `backend/app_basic_form/api/login_histories.py`
- 기존 스키마: `backend/database/schema.sql` (LoginHistory 테이블)
- **SQLite 스키마 설계**: `backend/app_new_form/SQLITE_LOGIN_HISTORY_SCHEMA.md` (개인정보 제외 버전)

---

## 3. 로그인 방식 변경 (이메일/전화번호)

### 현재 상태

**신규 ERD 구조 (`app_new_form`):**
- `user.u_id VARCHAR(50) UNIQUE` - 로그인 ID 기반 인증
- `user.u_phone VARCHAR(30) UNIQUE` - 전화번호 (UNIQUE 제약)
- 현재는 `u_id`만으로 로그인

**기존 구조 (`app_basic_form`):**
- `Customer.cEmail VARCHAR(255) UNIQUE` - 이메일 기반 인증
- `Customer.cPhoneNumber VARCHAR(50) UNIQUE` - 전화번호 (UNIQUE 제약)

---

### 💡 변경 예정 사항

**이메일과 전화번호를 유니크 키로 로그인 방식 변경 검토 중**

#### 현재 구조
```sql
CREATE TABLE user (
  u_seq      INT AUTO_INCREMENT PRIMARY KEY,
  u_id       VARCHAR(50)  NOT NULL UNIQUE COMMENT '고객 로그인 ID',
  u_password VARCHAR(255) NOT NULL,
  u_name     VARCHAR(255) NOT NULL,
  u_phone    VARCHAR(30)  NOT NULL UNIQUE COMMENT '고객 전화번호',
  ...
);
```

#### 변경 예정 구조 (검토 중)
```sql
-- 옵션 1: 이메일 필드 추가
ALTER TABLE user 
  ADD COLUMN u_email VARCHAR(255) UNIQUE COMMENT '고객 이메일';

-- 옵션 2: u_id를 이메일/전화번호로 확장
-- u_id 또는 u_phone으로 로그인 가능하도록 변경
```

---

### 📝 논의 사항

#### 결정 필요 사항

1. **로그인 방식**
   - 이메일로 로그인 가능하게 할 것인가?
   - 전화번호로 로그인 가능하게 할 것인가?
   - 둘 다 가능하게 할 것인가?
   - 현재 `u_id` 방식 유지할 것인가?

2. **데이터 구조**
   - `u_email` 필드 추가 필요 여부
   - `u_id`의 의미 변경 (이메일/전화번호/사용자 정의 ID)
   - 기존 `u_id` 데이터 마이그레이션 방법

3. **보안 고려사항**
   - 이메일/전화번호 인증 방식
   - 중복 가입 방지
   - 비밀번호 찾기 기능

4. **사용자 경험**
   - 로그인 편의성
   - 기존 사용자 영향도
   - 마이그레이션 계획

---

### 🔄 다음 단계

1. 개발팀과 논의 진행
2. 로그인 방식 결정
3. 스키마 수정 계획 수립
4. API 수정 및 구현
5. 테스트 및 배포

---

### 📌 참고

- 현재 구조: `backend/database/renew/shoes_shop_db_mysql_init_improved.sql`
- 현재 API: `backend/app_new_form/api/users.py`
- 기존 구조: `backend/database/schema.sql` (Customer.cEmail)

