# 새로운 ERD 구조 데이터베이스 스키마 및 개선사항

**작성일**: 2025-01-XX  
**목적**: 새로운 ERD 구조에 맞춘 개선된 MySQL 스키마 및 관련 문서

---

## 📁 파일 목록

### 1. 스키마 파일

#### `shoes_shop_db_mysql_init_improved.sql`
- **용도**: 새로운 ERD 구조에 맞춘 개선된 전체 스키마
- **개선사항**:
  - 인덱스 추가 (조회 성능 향상)
  - NOT NULL 제약조건 추가 (데이터 무결성)
  - UNIQUE 제약조건 추가 (중복 방지)
  - FOREIGN KEY CASCADE 옵션 명시
  - 데이터 타입 길이 조정
- **사용법**: 
  ```bash
  mysql -h [host] -P [port] -u [user] -p < shoes_shop_db_mysql_init_improved.sql
  ```
- **주의**: 이 파일은 전체 스키마를 DROP하고 재생성하므로, 기존 데이터가 있으면 백업 필요

---

### 2. 분석 및 비교 문서

#### `schema_comparison.md`
- **용도**: 기존 스키마와 새로운 스키마의 상세 비교 분석
- **내용**:
  - 주요 차이점 및 문제점
  - 인덱스, 제약조건 비교
  - 개선 권장사항
  - 종합 평가

#### `schema_issues_summary.md`
- **용도**: 스키마 문제점 요약
- **내용**:
  - 즉시 수정 필요 사항 (Critical)
  - 수정 권장 사항 (Important)
  - 개선 사항

---

### 3. 테스트 및 검증

#### `test_results.md`
- **용도**: 개선된 스키마 테스트 결과 리포트
- **내용**:
  - 인덱스 적용 상태
  - 제약조건 테스트 결과
  - 데이터 삽입 테스트
  - 성능 개선 예상치

#### `test_b_tnum_grouping.py`
- **용도**: `b_tnum`을 이용한 주문 그룹화 기능 테스트 스크립트
- **실행법**:
  ```bash
  python3 test_b_tnum_grouping.py
  ```

---

### 4. 사용 가이드

#### `b_tnum_usage_guide.md`
- **용도**: `b_tnum` (트랜잭션 번호) 사용 가이드
- **내용**:
  - `b_tnum`의 주문 그룹화 기능 설명
  - 사용 예시 및 SQL 쿼리
  - 기존 구조와의 비교
  - 주의사항 및 베스트 프랙티스

---

## 🚀 빠른 시작

### 1. 데이터베이스 생성

```bash
# 개선된 스키마로 데이터베이스 생성
mysql -h cheng80.myqnapcloud.com -P 13306 -u team0101 -p < shoes_shop_db_mysql_init_improved.sql
```

**주의**: 이 스크립트는 기존 데이터베이스를 DROP하고 재생성하므로, 기존 데이터가 있으면 먼저 백업하세요.

### 2. 테스트 실행

```bash
# b_tnum 그룹화 기능 테스트
python3 test_b_tnum_grouping.py
```

---

## 📊 주요 개선사항 요약

### ✅ 적용된 개선사항

1. **인덱스 추가**
   - `user`: u_id, u_phone UNIQUE 인덱스
   - `purchase_item`: b_tnum, b_date, u_seq, br_seq, p_seq 인덱스
   - `product`: p_name, m_seq 및 카테고리 인덱스
   - 모든 카테고리 테이블: UNIQUE 인덱스

2. **제약조건 강화**
   - NOT NULL 제약조건 추가 (필수 필드)
   - UNIQUE 제약조건 추가 (중복 방지)
   - FOREIGN KEY CASCADE 옵션 명시

3. **데이터 타입 개선**
   - `user.u_name`: VARCHAR(50) → VARCHAR(255)
   - `staff.s_rank`: VARCHAR(30) → VARCHAR(100)
   - `maker.m_name`: VARCHAR(100) → VARCHAR(255)

---

## 🔍 주요 변경사항

### 테이블 구조 변경

| 기존 구조 | 새로운 구조 |
|---------|-----------|
| `Customer` | `user` |
| `Employee` | `staff` (+ `branch` 연결) |
| `Manufacturer` | `maker` |
| `ProductBase` + `Product` | `product` (단일 테이블) |
| `Purchase` + `PurchaseItem` | `purchase_item` (단일 테이블 + `b_tnum`) |
| `ProductImage` | `product.p_image` (VARCHAR) |
| 없음 | `branch` (신규) |
| 없음 | 카테고리 테이블 4개 (신규) |
| 없음 | `pickup`, `refund`, `receive`, `request` (신규) |

---

## 📝 참고사항

### b_tnum 사용법

`b_tnum`은 여러 `purchase_item`을 하나의 주문으로 묶는 용도로 사용됩니다.

**예시**:
```sql
-- 같은 주문의 모든 항목에 동일한 b_tnum 부여
INSERT INTO purchase_item (..., b_tnum) VALUES (..., 'TXN-20250101-001');
INSERT INTO purchase_item (..., b_tnum) VALUES (..., 'TXN-20250101-001');

-- 주문 목록 조회
SELECT b_tnum, COUNT(*), SUM(b_price * b_quantity)
FROM purchase_item
WHERE u_seq = 1
GROUP BY b_tnum;
```

자세한 내용은 `b_tnum_usage_guide.md` 참조

---

## ✅ 검증 완료

- ✅ 인덱스 적용 확인
- ✅ 제약조건 테스트 완료
- ✅ 데이터 삽입 테스트 성공
- ✅ b_tnum 그룹화 기능 검증

---

## 📚 관련 문서

- `schema_comparison.md` - 상세 비교 분석
- `schema_issues_summary.md` - 문제점 요약
- `test_results.md` - 테스트 결과 리포트
- `b_tnum_usage_guide.md` - b_tnum 사용 가이드

