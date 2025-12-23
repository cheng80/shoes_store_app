# MySQL Database Schema and Dummy Data

이 폴더에는 MySQL 8.0.44용 데이터베이스 스키마와 더미 데이터 SQL 파일이 포함되어 있습니다.

## 파일 구조

- **`init.sql`** ⭐ **권장**: 전체 초기화 스크립트 (데이터베이스 생성 + 테이블 생성 + 더미 데이터 삽입)
- `schema.sql`: 데이터베이스 스키마 생성 파일 (테이블, 인덱스, 외래키 제약조건)
- `dummy_data.sql`: 개발용 더미 데이터 삽입 파일
- `reset.sql`: 기존 데이터 및 테이블 삭제 스크립트 (초기화)
- `README.md`: 이 문서

## 사용 방법

### 방법 1: MySQL Workbench 사용 (권장)

#### 전체 초기화 (가장 간단)

1. MySQL Workbench 실행
2. `File` > `Open SQL Script...` 선택
3. `backend/database/init.sql` 파일 선택
4. **번개 아이콘(Execute) 클릭** 또는 `Ctrl+Shift+Enter`
   - ⚠️ **중요**: 특정 라인을 선택하지 않고 번개 아이콘을 누르면 **전체 파일이 순차적으로 실행**됩니다
   - 파일 내부에 `USE shoes_store_db;`가 포함되어 있어 데이터베이스 선택은 자동으로 처리됩니다

**실행 순서**:
1. 데이터베이스 생성 (`CREATE DATABASE IF NOT EXISTS shoes_store_db`)
2. 데이터베이스 선택 (`USE shoes_store_db`)
3. 기존 테이블 및 데이터 삭제
4. 테이블 생성 (9개 테이블)
5. 더미 데이터 삽입

**실행 결과 확인**:
- 하단의 "Output" 탭에서 각 쿼리 실행 결과 확인 가능
- 오류 발생 시 해당 지점에서 중단되며, 이후 쿼리는 실행되지 않음

#### 단계별 실행

1. **초기화만** (데이터 삭제):
   - `reset.sql` 파일 실행

2. **스키마만** (테이블 생성):
   - `schema.sql` 파일 실행

3. **더미 데이터만** (데이터 삽입):
   - `dummy_data.sql` 파일 실행

### 방법 2: 명령줄 사용

```bash
# 전체 초기화
mysql -u root -p < backend/database/init.sql

# 또는 단계별 실행
mysql -u root -p
CREATE DATABASE IF NOT EXISTS shoes_store_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shoes_store_db;
SOURCE backend/database/schema.sql;
SOURCE backend/database/dummy_data.sql;
```

## 스키마 구조

### 테이블 목록

1. **Manufacturer** (제조사)
2. **ProductBase** (제품 기본 정보)
3. **ProductImage** (제품 이미지)
4. **Product** (제품 - 사이즈별 가격 및 재고)
5. **Customer** (고객)
6. **Employee** (직원/관리자)
7. **Purchase** (주문)
8. **PurchaseItem** (주문 항목)
9. **LoginHistory** (로그인 이력)

### 주요 특징

- **외래키 제약조건**: 모든 관계가 `ON DELETE CASCADE`로 설정되어 있어 부모 레코드 삭제 시 자식 레코드도 자동 삭제됩니다.
- **인덱스**: 조인 쿼리 성능 향상을 위한 인덱스가 포함되어 있습니다.
- **문자 인코딩**: `utf8mb4` 문자셋과 `utf8mb4_unicode_ci` 콜레이션을 사용하여 한글 및 이모지 지원이 가능합니다.

## 더미 데이터

`dummy_data.sql` 파일에는 개발용 더미 데이터가 포함되어 있습니다:

- **제조사**: Nike, NewBalance (2개)
- **제품 기본 정보**: 12개 제품 (U740WN2, 나이키 샥스 TL, 나이키 에어포스 1, 나이키 페가수스 플러스 × 각각 Black/Gray/White)
- **제품**: 각 제품 기본 정보당 7개 사이즈 (220~280) = 총 84개 제품
- **고객**: 6명
- **직원**: 3명
- **주문**: 5건
- **주문 항목**: 6개
- **로그인 이력**: 6건

## 주의사항

1. **외래키 체크**: `schema.sql`에서는 외래키 체크를 비활성화하여 테이블 삭제를 수행하지만, `dummy_data.sql`에서는 다시 활성화합니다.
2. **ID 자동 증가**: 모든 테이블의 ID는 `AUTO_INCREMENT`로 설정되어 있어 삽입 순서에 따라 자동으로 증가합니다.
3. **더미 데이터 순서**: 더미 데이터는 외래키 관계를 고려하여 올바른 순서로 삽입됩니다:
   - Manufacturer → ProductBase → ProductImage → Product → Customer → Employee → Purchase → PurchaseItem → LoginHistory

## FastAPI 연결 설정

`backend/app/database/connection.py`에서 데이터베이스 연결 설정을 확인하세요:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'shoes_store_db',
    'charset': 'utf8mb4'
}
```

## 문제 해결

### 외래키 제약조건 오류

만약 외래키 제약조건 오류가 발생하면:

```sql
SET FOREIGN_KEY_CHECKS = 0;
-- 스키마 또는 데이터 삽입 실행
SET FOREIGN_KEY_CHECKS = 1;
```

### 문자 인코딩 문제

MySQL 설정에서 `utf8mb4`를 지원하는지 확인:

```sql
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';
```

## 참고

- SQLite 스키마는 `lib/database/core/database_manager.dart`에 정의되어 있습니다.
- 더미 데이터는 `lib/database/dummy_data/` 폴더의 Dart 코드에서 생성됩니다.
- 이 SQL 파일들은 SQLite 스키마를 MySQL 8.0.44에 맞게 변환한 것입니다.

