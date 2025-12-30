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

## 🚀 빠른 시작

### 1. 데이터베이스 생성

```bash
# 개선된 스키마로 데이터베이스 생성
mysql -h cheng80.myqnapcloud.com -P 13306 -u team0101 -p < shoes_shop_db_mysql_init_improved.sql
```

**주의**: 이 스크립트는 기존 데이터베이스를 DROP하고 재생성하므로, 기존 데이터가 있으면 먼저 백업하세요.

---

## 📊 주요 개선사항 요약

### ✅ 적용된 개선사항

1. **인덱스 추가**
   - `user`: u_id, u_phone UNIQUE 인덱스
   - `purchase_item`: b_date, u_seq, br_seq, p_seq 인덱스
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
| `Purchase` + `PurchaseItem` | `purchase_item` (단일 테이블, 날짜 기반 그룹핑) |
| `ProductImage` | `product.p_image` (VARCHAR) |
| 없음 | `branch` (신규) |
| 없음 | 카테고리 테이블 4개 (신규) |
| 없음 | `pickup`, `refund`, `receive`, `request` (신규) |

---

---

## 📚 관련 문서

- `DOCS/SCREEN_API_MAPPING_SUMMARY.md` - 화면별 개발 가이드 (최소 버전)
- `DOCS/SCREEN_API_MAPPING_DETAIL.md` - 화면별 개발 가이드 (상세 버전)
- `DOCS/TASK_DISTRIBUTION_FINAL.md` - 최종 작업 분담

