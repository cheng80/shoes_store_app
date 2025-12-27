# 커밋 메시지

## 주요 변경사항

### 1. 프로필 이미지 기능 추가
- `app/api/customers.py`, `app/api/employees.py`
  - INSERT: 이미지 포함 필수 (Form + UploadFile)
  - UPDATE: 이미지 제외/포함 두 가지 방식 제공
  - 이미지 조회: Response 객체로 바이너리 직접 반환 (base64 제거)

### 2. 테스트 코드 개선
- `app/TEST/test_api.py`: 이미지 업로드 헬퍼 함수 추가, 랜덤 값 사용으로 중복 데이터 문제 해결
- `app/TEST/API_TEST_RESULTS.md`: 테스트 결과 문서화 (100% 성공)

### 3. 데이터베이스 스키마 업데이트
- Customer, Employee 테이블에 프로필 이미지 컬럼 추가 (MEDIUMBLOB)
- `init.sql`, `dummy_data.sql` 업데이트

### 4. 학습용 API 폴더 추가
- `app_basic_form/`: Form 방식 학습용 단순화 API
- `app_basic_model/`: JSON Body (Pydantic) 방식 학습용 단순화 API

---

## 간결한 커밋 메시지 (권장)

```
feat: 프로필 이미지 기능 추가 및 테스트 개선

- Customer/Employee 프로필 이미지 CRUD 기능 추가
  - INSERT: 이미지 포함 필수
  - UPDATE: 이미지 제외/포함 두 가지 방식
  - 이미지 조회: Response 객체로 바이너리 직접 반환
- 테스트 코드 개선: 랜덤 값 사용으로 중복 데이터 문제 해결
- 학습용 API 폴더 추가: app_basic_form, app_basic_model
- 데이터베이스 스키마 업데이트: 프로필 이미지 컬럼 추가
```

---

## 더 간결한 버전

```
feat: 프로필 이미지 기능 추가 및 테스트 개선

- Customer/Employee 프로필 이미지 CRUD 추가
- 테스트 코드 개선 (랜덤 값 사용, 중복 데이터 문제 해결)
- 학습용 API 폴더 추가 (app_basic_form, app_basic_model)
- DB 스키마 업데이트 (프로필 이미지 컬럼 추가)
```

